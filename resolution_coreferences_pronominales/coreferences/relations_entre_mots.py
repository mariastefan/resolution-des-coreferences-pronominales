from resolution_coreferences_pronominales.coreferences import mot


# Paramètres :
# mots : liste des mots qui nous intéressent, ex : ["eau", "rivière", "profond"]
# cache : True si on veut utiliser le cache, False sinon
# Retourne une liste avec toutes les relations entre les mots de la liste
def relations_entre_mots(mots: list, cache: bool):
    relations_mots_liste = []
    for i in range(len(mots)):
        mots_inexistants = []
        mot_dico = mot.relations_mot(mots[i], 'all', cache)
        while mot_dico is None and i < len(mots):
            mots_inexistants.append(i)
            i += 1
            mot_dico = mot.relations_mot(mots[i], 'all', cache)
        for j in range(len(mots)):
            if j != i and j not in mots_inexistants:
                for relation in mot_dico:
                    if mots[j] in relation:
                        trouve = 0
                        for k in range(len(relations_mots_liste)):
                            if mots[i] == relations_mots_liste[k][0] and mots[j] == relations_mots_liste[k][1] and \
                                    relation[3] == 'sortante':
                                relations_mots_liste[k][2][int(relation[1])] = relation[2]
                                trouve = 1
                            elif mots[j] == relations_mots_liste[k][0] and mots[i] == relations_mots_liste[k][1] and \
                                    relation[3] == 'entrante':
                                relations_mots_liste[k][2][int(relation[1])] = relation[2]
                                trouve = 1
                        if trouve == 0:
                            if relation[3] == 'sortante':
                                relations_mots_liste.append([mots[i], mots[j], {int(relation[1]): relation[2]}])
                            else:
                                relations_mots_liste.append([mots[j], mots[i], {int(relation[1]): relation[2]}])
    return relations_mots_liste
