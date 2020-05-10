from statistics import mean

import spacy
import extraction_mot


# Prend une phrase et retourne des informations sur ses pronoms
# Tous les mots sont lemmatisés
# obj/obl : à quoi fait référence le verbe (ex : "Le chien s'est cassé le museau", "museau" : obj de "cassé")
# ROOT : le verbe (racine)
# xcomp : complément qui donne du sens au verbe (ex : "Le chien va(ROOT) retenir(xcomp) la leçon")
# sens : relation sortante/entrante (ex : "Le chien est tombé dans le puits. Il est(sortante) profond.")
# Rend infos, une liste de taille 3 composé de :
# infos[0] = le pronom (str)
# infos[1] = [antécédents possibles] (list)
# infos[2] = {d'autres infos sur le pronom, comme le verbe, le COD...} (dictionary)
def informations_pronoms(phrase: str or spacy.tokens.doc.Doc):
    # Nous vérifions si phrase est de type spacy.tokens.doc.Doc pour gagner du temps (car spacy.load('fr') est lent)
    if isinstance(phrase, str):
        nlp = spacy.load('fr')
        doc = nlp(phrase)
    else:
        doc = phrase

    infos = []
    i = 0
    j = 0

    # Retourne les antécédents d'un pronom dans une phrase
    def antecedents(doc_tmp, m):
        antecedents_tmp = []
        noms_ant = []
        k = 0
        for jeton_aux in doc_tmp:
            k += 1
            if jeton_aux.pos_ == 'NOUN' or jeton_aux.pos_ == 'PROPN':
                noms_ant.extend([jeton_aux.lemma_])
            if m == k:
                antecedents_tmp.extend(noms_ant)
                break
        return antecedents_tmp

    for mot in doc:
        if mot.pos_ == 'PRON':
            pronom = mot
            infos.append([])
            infos[j].append(pronom.lemma_)

            # On ajoute à infos les antécédents du pronom
            infos[j].append(antecedents(doc, i))

            infos[j].append({})
            for nb_mots_restant in range(i, len(doc)):
                mot_2 = doc[nb_mots_restant]
                # cop : copula : mot dont la fonction est de lier l'attribut au sujet
                # d'une proposition (Il "est" profond.)
                if mot_2.pos_ == 'VERB' or mot_2.dep_ == 'cop':
                    verbe_trouve = False
                    complement_trouve = False
                    nb_mots_restant_suite = nb_mots_restant + 1
                    # Simule une boucle do while
                    while True:
                        # if doc[nb_mots_restant_suite].dep_ == 'obj'
                        if doc[nb_mots_restant_suite].dep_ == 'obj' or doc[nb_mots_restant_suite].dep_ == 'obl':
                            infos[j][2][doc[nb_mots_restant_suite].dep_] = doc[nb_mots_restant_suite].lemma_
                            complement_trouve = True
                        # 'Il va retenir la leçon.' xcomp va donner 'retenir' au lieu de 'aller'
                        elif doc[nb_mots_restant_suite].dep_ == 'xcomp':
                            infos[j][2][mot_2.dep_] = mot_2.lemma_
                            infos[j][2][doc[nb_mots_restant_suite].dep_] = doc[nb_mots_restant_suite].lemma_
                            if pronom.dep_ == 'nsubj' or 'expl':
                                infos[j][2]['sens'] = 'sortante'
                            elif pronom.dep_ == 'iobj':
                                infos[j][2]['sens'] = 'entrante'
                            verbe_trouve = True
                        if nb_mots_restant_suite == len(doc) - 1 or doc[nb_mots_restant_suite].dep_ == 'ROOT':
                            break
                        nb_mots_restant_suite += 1
                    if not verbe_trouve:
                        infos[j][2][mot_2.dep_] = mot_2.lemma_
                        if pronom.dep_ == 'nsubj' or 'expl':
                            infos[j][2]['sens'] = 'sortante'
                        elif pronom.dep_ == 'iobj':
                            infos[j][2]['sens'] = 'entrante'
                    break
            j += 1
        i += 1
    return infos


def coreferences_phrase(phrase: str or spacy.tokens.doc.Doc, cache: bool):
    # Nous vérifions si phrase est de type spacy.tokens.doc.Doc pour gagner du temps (car spacy.load('fr') est lent)
    if isinstance(phrase, str):
        nlp = spacy.load('fr')
        phrase = nlp(phrase)
    infos_pronoms = informations_pronoms(phrase)
    coreferences = []
    i = 1
    for infos_pour_un_pronom in infos_pronoms:
        pronom = infos_pour_un_pronom[0]
        dependances_pronom = []
        if 'xcomp' in infos_pour_un_pronom[2].keys():
            for key in infos_pour_un_pronom[2].keys():
                if key != 'sens' and key != 'ROOT':
                    dependances_pronom.append(infos_pour_un_pronom[2][key])
        else:
            for key in infos_pour_un_pronom[2].keys():
                if key != 'sens':
                    dependances_pronom.append(infos_pour_un_pronom[2][key])

        relations = extraction_mot.relations_entre_mots(infos_pour_un_pronom[1] + dependances_pronom, cache)
        if len(infos_pour_un_pronom[1]) == 1:
            coreferences.append([pronom, infos_pour_un_pronom[1][0]])
        elif infos_pour_un_pronom[2]['sens'] == 'sortante':
            relations_interessantes = {}
            for rel in relations:
                if rel[0] in infos_pour_un_pronom[1] and rel[1] in infos_pour_un_pronom[2].values():
                    relations_interessantes[(rel[0], rel[1])] = mean(rel[2].values())

            if len(relations_interessantes) == 0:
                # print("Attention, aucune relation intéressante n'a été trouvée sur jdm pour le pronom '" +
                #       str(i) + ':' + pronom +
                #       "', le premier antécédent a été gardé par défaut, à améliorer dans les prochaines versions.")
                coreferences.append([pronom, infos_pour_un_pronom[1][0]])
            elif len(relations_interessantes) == 1:
                coreferences.append([pronom, list(relations_interessantes.keys())[0][0]])
            else:
                poids_antecedents_ajoutes = {}
                for rel in relations_interessantes.keys():
                    if rel[0] not in poids_antecedents_ajoutes.keys():
                        poids_antecedents_ajoutes[rel[0]] = [relations_interessantes[rel], 1]
                    else:
                        poids_antecedents_ajoutes[rel[0]] = \
                            [poids_antecedents_ajoutes[rel[0]][0] + relations_interessantes[rel],
                             poids_antecedents_ajoutes[rel[0]][0] + 1]
                for a in poids_antecedents_ajoutes:
                    poids_antecedents_ajoutes[a] = poids_antecedents_ajoutes[a][0] / poids_antecedents_ajoutes[a][1]
                index = list(poids_antecedents_ajoutes.values()).index(max(poids_antecedents_ajoutes.values()))
                coreferences.append([pronom, list(poids_antecedents_ajoutes.keys())[index][0]])

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TOUS LES INDICES SONT À VERIFIER pour le cas entrant
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        elif infos_pour_un_pronom[2]['sens'] == 'entrante':
            relations_interessantes = {}
            for rel in relations:
                if rel[1] in infos_pour_un_pronom[1] and rel[0] in infos_pour_un_pronom[2].values():
                    relations_interessantes[(rel[0], rel[1])] = mean(rel[2].values())

            if len(relations_interessantes) == 0:
                # print("Attention, aucune relation intéressante n'a été trouvée sur jdm pour le pronom '" +
                #       str(i) + ':' + pronom +
                #       "', le premier antécédent a été gardé par défaut, à améliorer dans les prochaines versions.")
                coreferences.append([pronom, infos_pour_un_pronom[1][0]])
            elif len(relations_interessantes) == 1:
                coreferences.append([pronom, list(relations_interessantes.keys())[0][0]])
            else:
                poids_antecedents_ajoutes = {}
                for rel in relations_interessantes.keys():
                    if rel[0] not in poids_antecedents_ajoutes.keys():
                        poids_antecedents_ajoutes[rel[0]] = [relations_interessantes[rel], 1]
                    else:
                        poids_antecedents_ajoutes[rel[0]] = \
                            [poids_antecedents_ajoutes[rel[0]][0] + relations_interessantes[rel],
                             poids_antecedents_ajoutes[rel[0]][0] + 1]
                for a in poids_antecedents_ajoutes:
                    poids_antecedents_ajoutes[a] = poids_antecedents_ajoutes[a][0] / poids_antecedents_ajoutes[a][1]
                index = list(poids_antecedents_ajoutes.values()).index(max(poids_antecedents_ajoutes.values()))
                coreferences.append([pronom, list(poids_antecedents_ajoutes.keys())[index][0]])
        i += 1

    return coreferences


def affichier_antecedents_dans_phrase(phrase: str, cache: bool):
    nlp = spacy.load('fr')
    phrase = nlp(phrase)
    coreferences = coreferences_phrase(phrase, cache)
    phrase_antecedents = ''
    i = 0
    j = 0
    for mot in phrase:
        if str(mot) == '.' or j == 0:
            phrase_antecedents += str(mot)
        else:
            phrase_antecedents += ' ' + str(mot)
        if mot.pos_ == 'PRON':
            phrase_antecedents += '(' + coreferences[i][1] + ')'
            i += 1
        j += 1
    return phrase_antecedents
