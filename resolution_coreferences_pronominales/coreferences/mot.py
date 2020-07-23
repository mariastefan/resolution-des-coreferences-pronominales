import re
from time import sleep

from bs4 import BeautifulSoup
import requests
import os
import sys
import pickle
from resolution_coreferences_pronominales.coreferences import cache

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
    adresse = 'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='
    # adresse = 'http://0.0.0.0:3000/rezo-dump.php?gotermsubmit=Chercher&gotermrel='
    rq_word_converti = conversion_mot(rq_word)
    nombre_essais = 3
    while True:
        try:
            if type_relation == 'all':
                html = requests.get(adresse + rq_word_converti + '&rel=')
            else:
                html = requests.get(adresse + rq_word_converti + '&rel=' + type_relation)
            break

        except Exception as erreur:
            if not erreur.args:
                print('\033[36m' + '\nIl y a eu une erreur de connexion a jdm pour le mot ' +
                      '\033[4m' + rq_word + '\033[0m' + '\033[36m' + '. On réessaie.' + '\033[0m')
            else:
                print(str(erreur.args) + '\033[36m' + '\nIl y a eu une erreur de connexion a jdm pour le mot ' +
                      '\033[4m' + rq_word + '\033[0m' + '\033[36m' + '. On réessaie.' + '\033[0m')
            if nombre_essais == 0:
                sys.exit('Il y a eu trop de tentatives de connexion à jdm pour le mot ' + rq_word + '. Abandon.')
            else:
                sleep(1)
                pass
        nombre_essais -= 1

    # encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    div_warning_jdm = soup.find_all("div", {"class": "jdm-warning"})
    for div in div_warning_jdm:
        if '\'' + rq_word + '\'' + ' n\'existe pas' in div.text:
            print('Le mot \"' + rq_word + '" n\'existe pas dans jeuxdemots.org !')
            return None
    texte_brut = soup.find_all('code')
    return texte_brut


# Prend le mot, le type de la relation (pour toutes les relations alors type_relation = 'all') et cache (True ou False).
# Retourne une liste de listes des relations du mot, récupérées sur jeuxdemots.org, chaque sous-liste contenant dans
# l'ordre :
# - le nom de l'autre noeud
# - le numero du type de la relation
# - poids de la relation
# - sortante/entrante

def creation_tabs_noeuds_relations_mot(mot: str, type_relation: str):
    texte_brut = extraction_html(mot, type_relation)
    if texte_brut is None:
        return None, None
    lignes_noeuds_et_relations = re.findall('[re];[0-9]*;.*', str(texte_brut))
    if not lignes_noeuds_et_relations:
        print('Aucune relation pour le mot \'' + mot + '\'.')
        return None, None
    tab_eids = {}
    tab_rids = {}
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
    return tab_eids, tab_rids


def bornes_poids(tab_rids: dict):
    max_positif = 0
    min_negatif = 0
    for i in range(len(list(tab_rids.values()))):
        poids = int(list(tab_rids.values())[i][3])
        if poids >= 0 and poids > max_positif:
            max_positif = poids
        if poids < 0 and poids < min_negatif:
            min_negatif = poids
    return min_negatif, max_positif


def relations_mot(mot: str, type_relation: str, avec_cache: bool):
    def sans_cache(mot_tmp, type_relation_tmp):
        tab_eids, tab_rids = creation_tabs_noeuds_relations_mot(mot_tmp, type_relation_tmp)
        if tab_rids is None:
            return None

        relations_list = []
        min_negatif, max_positif = bornes_poids(tab_rids)

        for rid in list(tab_rids.keys()):
            poids = int(tab_rids[rid][3])
            if poids < 0:
                poids = (poids / min_negatif) * (-1)
            else:
                poids = poids / max_positif
            eid_mot = list(tab_eids.keys())[0]
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

        fichier_cache = cache.creer_fichier(mot_tmp, type_relation_tmp)
        if fichier_cache is None:
            sys.exit()
        pickle.dump(relations_list, fichier_cache)
        cache.fermer_fichier(fichier_cache)
        return relations_list

    if not avec_cache:
        return sans_cache(mot, type_relation)
    elif avec_cache and (not cache.existe() or not cache.contient_fichier(mot, type_relation)):
        return sans_cache(mot, type_relation)
    elif avec_cache:
        fichier = cache.ouvrir_fichier(mot, type_relation, 'rb')
        if fichier is None:
            sys.exit()
        relations = pickle.load(fichier)
        cache.fermer_fichier(fichier)
        return relations
    else:
        sys.exit('cache doit etre egal a True ou False')
