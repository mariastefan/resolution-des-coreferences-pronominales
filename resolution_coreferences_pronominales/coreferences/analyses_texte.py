from statistics import mean

import spacy
import fr_core_news_sm
from resolution_coreferences_pronominales.coreferences import relations_entre_mots
from spacy.matcher import Matcher


def nlp_loader():
    nlp = fr_core_news_sm.load()
    matcher = Matcher(nlp.vocab)
    matcher.add('HYPHENS', None, [{'IS_ALPHA': True}, {'ORTH': '-', 'OP': '+'}, {'IS_ALPHA': True}])
    liste = ['intelligence artificielle']
    for e in liste:
        zzz = []
        for i in e.split(" "):
            zzz.append({'ORTH': i})
        matcher.add(e, None, zzz)

    def quote_merger(doc):
        # this will be called on the Doc object in the pipeline
        matched_spans = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
        for span in matched_spans:  # merge into one token after collecting all matches
            span.merge()
        return doc

    nlp.add_pipe(quote_merger, first=True)  # add it right after the tokenizer
    return nlp

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
        nlp = nlp_loader()
        doc = nlp(phrase)
    else:
        doc = phrase

    infos = []
    k = 0
    i = 0
    for mot in doc:
        i += 1
        if mot.pos_ == 'PRON':
            infos.append([])
            pronom = mot
            verbe = pronom.head
            infos[k].append(pronom.text)
            infos[k].append([])
            infos[k].append({verbe.dep_: verbe.lemma_})

            # Si le pronom est un objet indirect ('iobj') alors la relation est entrante, sinon sortante
            if pronom.dep_ == 'iobj':
                infos[k][2]['sens'] = 'entrante'
            else:
                infos[k][2]['sens'] = 'sortante'

            if pronom.dep_ != 'iobj' and 'iobj' not in [enfant_verbe.dep_ for enfant_verbe in verbe.children]:
                for enfant_verbe in verbe.children:
                    # Nous enlevons 'nsubj' et 'expl' (pronoms) car nous avons déjà cette info, ainsi que
                    # les ponctuations
                    if enfant_verbe.dep_ != 'nsubj' and enfant_verbe.dep_ != 'expl' and enfant_verbe.dep_ != 'punct' \
                            and enfant_verbe.dep_ != 'aux' and enfant_verbe.dep_ != 'iobj' \
                            and enfant_verbe.dep_ != 'cop':
                        # Si l'enfant du verbe est un autre verbe qui le complète, alors on prend aussi ses enfants
                        if enfant_verbe.dep_ == 'xcomp':
                            infos[k][2][enfant_verbe.dep_] = [enfant_verbe.lemma_, {}]
                            for enfant_complement in enfant_verbe.children:
                                if enfant_verbe.dep_ != 'aux' and enfant_verbe.dep_ != 'cop':
                                    infos[k][2][enfant_verbe.dep_][1][enfant_complement.dep_] = enfant_complement.lemma_
                        elif enfant_verbe not in infos[k][2].keys():
                            infos[k][2][enfant_verbe.dep_] = enfant_verbe.lemma_
                        else:
                            infos[k][2][enfant_verbe.dep_] = [infos[k][2][enfant_verbe], enfant_verbe]
            else:
                if pronom.dep_ == 'iobj':
                    for enfant_verbe in verbe.children:
                        # Nous enlevons 'nsubj' et 'expl' (pronoms) car nous avons déjà cette info, ainsi que
                        # les ponctuations
                        if enfant_verbe.dep_ != 'nsubj' and enfant_verbe.dep_ != 'expl' \
                                and enfant_verbe.dep_ != 'punct' and enfant_verbe.dep_ != 'aux' \
                                and enfant_verbe.dep_ != 'iobj' and enfant_verbe.dep_ != 'cop':
                            # Si l'enfant du verbe est un autre verbe qui le complète, alors on prend aussi
                            # ses enfants
                            if enfant_verbe.dep_ == 'xcomp':
                                infos[k][2][enfant_verbe.dep_] = [enfant_verbe.lemma_, {}]
                                for enfant_complement in enfant_verbe.children:
                                    if enfant_verbe.dep_ != 'aux' and enfant_verbe.dep_ != 'cop':
                                        infos[k][2][enfant_verbe.dep_][1][
                                            enfant_complement.dep_] = enfant_complement.lemma_
                            elif enfant_verbe not in infos[k][2].keys():
                                infos[k][2][enfant_verbe.dep_] = enfant_verbe.lemma_
                            else:
                                infos[k][2][enfant_verbe.dep_] = [infos[k][2][enfant_verbe], enfant_verbe]
                    else:
                        for enfant_verbe in verbe.children:
                            # Nous enlevons 'nsubj' et 'expl' (pronoms) car nous avons déjà cette info, ainsi que
                            # les ponctuations
                            if enfant_verbe.dep_ != 'nsubj' and enfant_verbe.dep_ != 'expl' \
                                    and enfant_verbe.dep_ != 'punct' and enfant_verbe.dep_ != 'aux' \
                                    and enfant_verbe.dep_ != 'iobj' and enfant_verbe.dep_ != 'obj' \
                                    and enfant_verbe.dep_ != 'obl' and enfant_verbe.dep_ != 'cop':
                                # Si l'enfant du verbe est un autre verbe qui le complète, alors on prend aussi
                                # ses enfants
                                if enfant_verbe.dep_ == 'xcomp':
                                    infos[k][2][enfant_verbe.dep_] = [enfant_verbe.lemma_, {}]
                                    for enfant_complement in enfant_verbe.children:
                                        if enfant_verbe.dep_ != 'aux' and enfant_verbe.dep_ != 'cop':
                                            infos[k][2][enfant_verbe.dep_][1][
                                                enfant_complement.dep_] = enfant_complement.lemma_
                                elif enfant_verbe not in infos[k][2].keys():
                                    infos[k][2][enfant_verbe.dep_] = enfant_verbe.lemma_
                                else:
                                    infos[k][2][enfant_verbe.dep_] = [infos[k][2][enfant_verbe], enfant_verbe]

            # On fait une boucle jusqu'au pronom courant pour prendre tous les antécédents possibles du pronom
            j = 0
            for mot_aux in doc:
                j += 1
                # Nous prenons les adjectifs aussi car fr_core_news_sm n'est pas parfait
                if (mot_aux.pos_ == 'NOUN' or mot_aux.pos_ == 'PROPN' or mot_aux.pos_ == 'ADJ') \
                        and mot_aux.dep_ != 'case':
                    infos[k][1].append(mot_aux.lemma_)
                if i == j:
                    break
            k += 1
    return infos


def coreferences_phrase(phrase: str or spacy.tokens.doc.Doc, cache: bool):
    # Nous vérifions si phrase est de type spacy.tokens.doc.Doc pour gagner du temps (car spacy.load('fr') est lent)
    if isinstance(phrase, str):
        nlp = nlp_loader()
        phrase = nlp(phrase)
    infos_pronoms = informations_pronoms(phrase)
    coreferences = []
    i = 1
    for infos_pour_un_pronom in infos_pronoms:
        pronom = infos_pour_un_pronom[0]
        dependances_pronom = []

        # Si le verbe racine a un complément qui est un autre verbe ('xcomp') alors on ignore le verbe racine
        if 'xcomp' in infos_pour_un_pronom[2].keys():
            for key in infos_pour_un_pronom[2].keys():
                if key != 'xcomp' and isinstance(infos_pour_un_pronom[2][key], list):
                    for element in infos_pour_un_pronom[2][key]:
                        dependances_pronom.append(element)
                elif key == 'xcomp':
                    dependances_pronom.append(infos_pour_un_pronom[2][key][0])
                    for key_xcomp in infos_pour_un_pronom[2][key][1]:
                        dependances_pronom.append(infos_pour_un_pronom[2][key][1][key_xcomp])
                elif key != 'sens' and key != 'ROOT':
                    dependances_pronom.append(infos_pour_un_pronom[2][key])
        else:
            for key in infos_pour_un_pronom[2].keys():
                if isinstance(infos_pour_un_pronom[2][key], list):
                    for element in infos_pour_un_pronom[2][key]:
                        dependances_pronom.append(element)
                elif key != 'sens':
                    dependances_pronom.append(infos_pour_un_pronom[2][key])

        # S'il y a un seul antécédent possible pour le pronom alors on le choisit et on passe au prochain pronom
        if len(infos_pour_un_pronom[1]) == 1:
            coreferences.append([pronom, infos_pour_un_pronom[1][0]])
        else:
            # On cherche sur jdm toutes les relations possibles entre les antécédents potentiels du
            # pronom (infos_pour_un_pronom[1]) et les mots qui ont un lien avec le pronom (dependances_pronom)
            relations = relations_entre_mots.relations_entre_mots(infos_pour_un_pronom[1] + dependances_pronom, cache)

            relations_interessantes = {}

            # Pour chaque relation trouvée précédemment on ajoute à relations_interessantes celles dont le premier
            # noeud est dans la liste des antécédents possibles et le 2nd noeud dans les mots en lien avec le pronom
            for rel in relations:
                if rel[0] in infos_pour_un_pronom[1] and rel[1] in infos_pour_un_pronom[2].values():
                    relations_interessantes[(rel[0], rel[1])] = mean(rel[2].values())

            # Si aucune relation intéressante n'a été trouvée alors le premier antécédent de la liste des
            # antécédents possibles est gardé par défaut
            if len(relations_interessantes) == 0:
                coreferences.append([pronom, infos_pour_un_pronom[1][0]])

            # Si une seule relation intéressante est trouvée alors nous gardons l'antécédent impliqué
            # dans cette relation
            elif len(relations_interessantes) == 1:
                coreferences.append([pronom, list(relations_interessantes.keys())[0][0]])

            # Sinon on garde seulement une relation par antécédent potentiel et la moyenne des poids des
            # relations impliquant cet antécédent
            else:
                poids_antecedents_ajoutes = {}
                for rel in relations_interessantes.keys():
                    if rel[0] not in poids_antecedents_ajoutes.keys():
                        poids_antecedents_ajoutes[rel[0]] = [relations_interessantes[rel], 1]
                    else:
                        poids_antecedents_ajoutes[rel[0]] = \
                            [poids_antecedents_ajoutes[rel[0]][0] + relations_interessantes[rel],
                             poids_antecedents_ajoutes[rel[0]][1] + 1]
                for antecedent in poids_antecedents_ajoutes:
                    poids_antecedents_ajoutes[antecedent] = poids_antecedents_ajoutes[antecedent][0] / \
                                                            poids_antecedents_ajoutes[antecedent][1]
                index = list(poids_antecedents_ajoutes.values()).index(max(poids_antecedents_ajoutes.values()))
                coreferences.append([pronom, list(poids_antecedents_ajoutes.keys())[index]])

        i += 1

    return coreferences


def affichier_antecedents_dans_phrase(phrase: str, cache: bool):
    nlp = nlp_loader()
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
