import spacy

# Prend une phrase et retourne des informations sur ses pronoms
# Tous les mots sont lemmatisés
# obj/obl : à quoi fait référence le verbe (ex : "Le chien s'est cassé le museau", "museau" : obj de "cassé")
# ROOT : le verbe (racine)
# xcomp : complément qui donne du sens au verbe (ex : "Le chien va(ROOT) retenir(xcomp) la leçon")
# sens : relation sortante/entrante (ex : "Le chien est tombé dans le puits. Il est(sortante) profond.")
def infos_pronoms(phrase):
    nlp = spacy.load('fr')
    doc = nlp(phrase)

    infos = []
    i = 0
    j = 0

    # Retourne les antécédents d'un (seul) pronom dans une phrase
    def antecedents(pronom_tmp, doc_tmp, m):
        noms = []
        antecedents_tmp = []
        noms_ant = []
        k = 0
        for jetonAux in doc_tmp:
            k += 1
            if jetonAux.pos_ == 'NOUN' or jetonAux.pos_ == 'PROPN':
                noms_ant.extend([jetonAux])
                if 'nsubj' in jetonAux.dep_:
                    noms.append(['->', jetonAux, pronom_tmp.head])
                if jetonAux.dep_ == 'obj':
                    noms.append(['<-', jetonAux, pronom_tmp.head])
                if jetonAux.dep_ == 'amod':
                    noms.append([jetonAux, jetonAux.head])
            if m == k:
                antecedents_tmp.extend(noms_ant)
                break
        return antecedents_tmp

    for mot in doc:
        if mot.pos_ == 'PRON':
            pronom = mot
            infos.append([])
            infos[j].append(pronom.lemma_)

            # On ajoute à infos les antécédents de pronom
            infos[j].append(antecedents(pronom, doc, i))

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
                        if nb_mots_restant_suite == len(doc) - 1 or doc[nb_mots_restant_suite].pos_ == 'VERB':
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
