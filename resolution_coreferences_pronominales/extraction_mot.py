import re
from bs4 import BeautifulSoup
import requests
import os
import sys
import pickle


# Fonction permettant l'insertion du mot rq_word dans l'URL lors de la requete à jdm
# Il n'y a pas de raison d'utiliser cette fonction seule
def conversion_mot(rq_word: str):
    conversion_partielle = rq_word.encode('iso-8859-1')
    resultat = re.search("b[\"'](.*)[\"']$", str(conversion_partielle))
    resultat = resultat.group(1)
    resultat = resultat.replace("'", '%27')
    resultat = resultat.replace(' ', '+')
    resultat = resultat.replace('\\x', '%')
    return resultat


# Prend rq_word (mot recherché) et retourne le code html correspondant depuis http://www.jeuxdemots.org/rezo-dump
# Il n'y a pas de raison d'utiliser cette fonction seule
def extraction_html(rq_word: str, type_relation: str):
    rq_word_converti = conversion_mot(rq_word)
    if type_relation == 'all':
        html = requests.get(
            'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + rq_word_converti + '&rel=')
    else:
        html = requests.get(
            'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + rq_word_converti + '&rel=' +
            type_relation)
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    return texte_brut


# Prend le mot, le type de la relation (pour toutes les relations alors type_relation = 'all') et cache (True ou False).
# Retourne une liste de listes des relations du mot, récupérées sur jeuxdemots.org, chaque sous-liste contenant dans
# l'ordre :
# - le nom de l'autre noeud
# - le numero du type de la relation
# - poids de la relation
# - sortante/entrante
def relations_mot(mot: str, type_relation: str, cache: bool):
    def sans_cache(mot_tmp, type_relation_tmp):
        texte_brut = extraction_html(mot_tmp, type_relation_tmp)
        try:
            lignes_noeuds_et_relations = re.findall('[re];[0-9]*;.*', str(texte_brut))
            if not lignes_noeuds_et_relations:
                print('Le mot \"' + mot + ' n\'existe pas dans jeuxdemots.org')
                return None
        except ValueError as err:
            print(err)
            sys.exit()
        tab_eids = {}
        tab_rids = {}
        eid_mot = re.search('e;([0-9]*);.*', lignes_noeuds_et_relations[0]).group(1)
        stop = 0
        for a in lignes_noeuds_et_relations:
            if stop == 0:
                result_noeud = re.search("e;([0-9]*);(.*);(-*[0-9]*);(-*[0-9]*);*'*([^']*)'*", str(a))
                if result_noeud:
                    if len(tab_eids) != 0 and result_noeud.group(1) in tab_eids.keys():
                        raise KeyError('Probleme dans jdm : eid doit etre unique')
                    poids = result_noeud.group(4)
                    if not poids or poids == '':
                        poids = '0'
                    # J'enlève les guillemets si présentes
                    autre_noeud = result_noeud.group(2).strip("''")
                    tab_eids[result_noeud.group(1)] = [autre_noeud,
                                                       result_noeud.group(3),
                                                       poids,
                                                       result_noeud.group(5)]
            result_rel = re.search("r;([0-9]*);([0-9]*);([0-9]*);([0-9]*);(-*[0-9]*)", str(a))
            if result_rel:
                stop = 1
                poids = result_rel.group(5)
                if not poids or poids == '':
                    poids = '0'
                if len(tab_rids) != 0 and result_rel.group(1) in tab_rids.keys():
                    del tab_rids[result_rel.group(1)]
                    tab_rids[result_rel.group(1) + '_entrante'] = [result_rel.group(2),
                                                                   result_rel.group(3),
                                                                   result_rel.group(4),
                                                                   poids,
                                                                   'entrante+sortante']
                    tab_rids[result_rel.group(1) + '_sortante'] = [result_rel.group(2),
                                                                   result_rel.group(3),
                                                                   result_rel.group(4),
                                                                   poids,
                                                                   'entrante+sortante']
                else:
                    tab_rids[result_rel.group(1)] = [result_rel.group(2),
                                                     result_rel.group(3),
                                                     result_rel.group(4),
                                                     poids]
                    if result_rel.group(1) not in tab_rids.keys():
                        raise KeyError(
                            'Création tab_rids : la cref ' + str(result_rel.group(1)) + ' n\'a pas pu etre créée')
        max_positif = 0
        min_negatif = 0
        for i in range(len(list(tab_rids.values()))):
            poids = int(list(tab_rids.values())[i][3])
            if poids >= 0 and poids > max_positif:
                max_positif = poids
            if poids < 0 and poids < min_negatif:
                min_negatif = poids

        relations_list = []

        for rid in list(tab_rids.keys()):
            poids = int(tab_rids[rid][3])
            if poids < 0:
                poids = (poids / min_negatif) * (-1)
            else:
                poids = poids / max_positif

            if tab_rids[rid][0] == eid_mot:
                relations_list.append([tab_eids[tab_rids[rid][1]][0],
                                       tab_rids[rid][2],
                                       poids,
                                       'sortante'])
            elif tab_rids[rid][1] == eid_mot:
                relations_list.append([tab_eids[tab_rids[rid][0]][0],
                                       tab_rids[rid][2],
                                       poids,
                                       'entrante'])
        chemin_absolu = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(chemin_absolu + '/cache'):
            try:
                os.mkdir(chemin_absolu + '/cache')
            except OSError:
                print('La création du dossier cache a échoué')
        fichier_cache = open(chemin_absolu + '/cache/' + mot_tmp + '_' + type_relation_tmp + '.pkl', 'wb')
        pickle.dump(relations_list, fichier_cache)
        fichier_cache.close()
        return relations_list

    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if not cache:
        return sans_cache(mot, type_relation)
    elif cache and (
            not os.path.isdir(chemin_absolu + '/cache') or not os.path.isfile(
        chemin_absolu + '/cache/' + mot + '_' + type_relation + '.pkl')):
        return sans_cache(mot, type_relation)
    elif cache:
        fichier = open(chemin_absolu + '/cache/' + mot + '_' + type_relation + '.pkl', 'rb')
        relations = pickle.load(fichier)
        fichier.close()
        return relations
    else:
        sys.exit('cache doit etre egal a True ou False')


# Paramètres :
# mots : liste des mots qui nous intéressent, ex : ["eau", "rivière", "profond"]
# cache : True si on veut utiliser le cache, False sinon
# Retourne une liste avec toutes les relations entre les mots de la liste
def relations_entre_mots(mots: list, cache: bool):
    relations_mots_liste = []
    for i in range(len(mots) - 1):
        mot_dico = relations_mot(mots[i], 'all', cache)
        if mot_dico is None:
            i += 1
        for j in range(i + 1, len(mots)):
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


# Supprime les fichiers existants dans le dossier cache
def vider_cache():
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(chemin_absolu + '/cache'):
        for filename in os.listdir(chemin_absolu + '/cache'):
            chemin_fichier = os.path.join(chemin_absolu + '/cache', filename)
            try:
                os.remove(chemin_fichier)
            except Exception as e:
                print('Impossible de supprimer le fichier %s. Motif : %s' % (chemin_fichier, e))


# Supprime le dossier cache
def supprimer_cache():
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(chemin_absolu + '/cache'):
        if len(os.listdir(chemin_absolu + '/cache')) != 0:
            vider_cache()
        try:
            os.rmdir(chemin_absolu + '/cache')
        except Exception as e:
            print('Impossible de supprimer le dossier cache. Motif : %s' % e)
