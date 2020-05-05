import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import sys
import pickle


# Fonction permettant l'insertion du mot rq_word dans l'URL lors de la requete à jdm
# Appelée seulement dans extraction_html
def conversion_mot(rq_word: str):
    conversion_partielle = rq_word.encode('iso-8859-1')
    resultat = re.search("b[\"'](.*)[\"']$", str(conversion_partielle))
    resultat = resultat.group(1)
    resultat = resultat.replace("'", '%27')
    resultat = resultat.replace('\\x', '%')
    return resultat


# Prend rq_word (mot recherché) et retourne le code html correspondant depuis http://www.jeuxdemots.org/rezo-dump
def extraction_html(rq_word: str, type_relation: str):
    rq_word_converti = conversion_mot(rq_word)
    if type_relation == 'all':
        html = requests.get(
            'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + rq_word_converti + '&rel=')
    else:
        html = requests.get(
            'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + rq_word_converti + '&rel=' +
            type_relation)
    encoding = html.encoding if "charset" in html.headers.get("content-type", "").lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    return texte_brut


# Prend le mot ainsi que le type de la relation (pour toutes les relations alors type_relation = 'all').
# Retourne un tableau DataFrame avec les colonnes 'id_relation', 'lautre_noeud', 'type_relation',
# 'poids_relation', 'sens_relation'
# Ce tableau contient les relations sortantes et entrantes du mot, récupérées depuis jdm.

def old_relations_mot(mot: str, type_relation: str, cache: int):
    def sans_cache(mot_tmp, type_relation_tmp):
        texte_brut = extraction_html(mot_tmp, type_relation_tmp)
        tab_eids = pd.DataFrame(columns=('eid', 'name', 'type', 'w', 'formatted name'))
        tab_rids = pd.DataFrame(columns=('rid', 'node1', 'node2', 'type', 'w'))
        lignes_noeuds_et_relations = re.findall("[re];[0-9]*;.*", str(texte_brut))
        stop = 0
        for a in lignes_noeuds_et_relations:
            if stop == 0:
                result_noeud = re.search("e;([0-9]*);'(.*)';([0-9]*);([0-9]*);*'*([^']*)'*", str(a))
                if result_noeud:
                    poids = result_noeud.group(4)
                    if not poids or poids == '':
                        poids = '0'
                    tab_eids = tab_eids.append(pd.DataFrame({"eid": [result_noeud.group(1)],
                                                             "name": [result_noeud.group(2)],
                                                             "type": [result_noeud.group(3)],
                                                             "w": [poids],
                                                             "formatted name": [result_noeud.group(5)]
                                                             }), ignore_index=True)
            result_rel = re.search("r;([0-9]*);([0-9]*);([0-9]*);([0-9]*);([0-9]*)", str(a))
            if result_rel:
                stop = 1
                poids = result_rel.group(5)
                if not poids or poids == '':
                    poids = '0'
                tab_rids = tab_rids.append(pd.DataFrame({"rid": [result_rel.group(1)],
                                                         "node1": [result_rel.group(2)],
                                                         "node2": [result_rel.group(3)],
                                                         "type": [result_rel.group(4)],
                                                         "w": [poids]
                                                         }), ignore_index=True)
        tab_eids['w'] = tab_eids['w'].astype(int) / max(tab_eids['w'].astype(int))
        tab_rids['w'] = tab_rids['w'].astype(int) / max(tab_rids['w'].astype(int))

        relations = pd.DataFrame(
            columns=('id_relation', 'lautre_noeud', 'type_relation', 'poids_relation', 'sens_relation'))

        for i in range(tab_rids.shape[0]):
            if tab_rids['node1'][i] == tab_eids['eid'][0]:
                relations = relations.append(pd.DataFrame({
                    'id_relation': [tab_rids['rid'][i]],
                    'lautre_noeud': tab_eids['name'][tab_eids.loc[tab_eids['eid'] == tab_rids['node2'][i]].index[0]],
                    'type_relation': [tab_rids['type'][i]],
                    'poids_relation': [tab_rids['w'][i]],
                    'sens_relation': 'sortante'
                }, index=[i]))
            else:
                relations = relations.append(pd.DataFrame({
                    'id_relation': [tab_rids['rid'][i]],
                    'lautre_noeud': tab_eids['name'][tab_eids.loc[tab_eids['eid'] == tab_rids['node1'][i]].index[0]],
                    'type_relation': [tab_rids['type'][i]],
                    'poids_relation': [tab_rids['w'][i]],
                    'sens_relation': 'entrante'
                }, index=[i]))
        if not os.path.isdir('./cache'):
            try:
                os.mkdir("./cache")
            except OSError:
                print("Creation of the directory cache failed")
        relations.to_csv('./cache/' + mot_tmp + '_' + type_relation_tmp + '.csv', sep='\t')
        return relations

    if cache == 0:
        return sans_cache(mot, type_relation)
    elif cache == 1 and (
            not os.path.isdir('./cache') or not os.path.isfile('./cache/' + mot + '_' + type_relation + '.csv')):
        return sans_cache(mot, type_relation)
    elif cache == 1:
        return pd.read_csv('./cache/' + mot + '_' + type_relation + '.csv')
    else:
        sys.exit("cache doit etre egal a 0 ou 1")


def relations_mot(mot: str, type_relation: str, cache: int):
    def sans_cache(mot_tmp, type_relation_tmp):
        texte_brut = extraction_html(mot_tmp, type_relation_tmp)
        tab_eids = {}
        tab_rids = {}
        lignes_noeuds_et_relations = re.findall("[re];[0-9]*;.*", str(texte_brut))
        stop = 0
        for a in lignes_noeuds_et_relations:
            if stop == 0:
                result_noeud = re.search("e;([0-9]*);'(.*)';([0-9]*);([0-9]*);*'*([^']*)'*", str(a))
                if result_noeud:
                    poids = result_noeud.group(4)
                    if not poids or poids == '':
                        poids = '0'
                    tab_eids[result_noeud.group(1)] = [result_noeud.group(2),
                                                       result_noeud.group(3),
                                                       poids,
                                                       result_noeud.group(5)]
            result_rel = re.search("r;([0-9]*);([0-9]*);([0-9]*);([0-9]*);([0-9]*)", str(a))
            if result_rel:
                stop = 1
                poids = result_rel.group(5)
                if not poids or poids == '':
                    poids = '0'
                tab_rids[result_rel.group(1)] = [result_rel.group(2),
                                                 result_rel.group(3),
                                                 result_rel.group(4),
                                                 poids]
        max_positif = 0
        min_negatif = 0
        for i in range(len(list(tab_rids.values()))):
            poids = int(list(tab_rids.values())[i][3])
            if poids >= 0 and poids > max_positif:
                max_positif = poids
            if poids < 0 and poids < min_negatif:
                min_negatif = poids

        relations = {}

        for rid in list(tab_rids.keys()):
            poids = int(tab_rids[rid][3])
            if poids < 0:
                poids = (poids / min_negatif) * (-1)
            else:
                poids = poids / max_positif
            for eid in list(tab_eids.keys()):
                if tab_rids[rid][0] == eid:
                    relations[rid] = [tab_eids[tab_rids[rid][0]][0],
                                      tab_rids[rid][2],
                                      poids,
                                      'sortante']
                elif tab_rids[rid][1] == eid:
                    relations[rid] = [tab_eids[tab_rids[rid][1]][0],
                                      tab_rids[rid][2],
                                      poids,
                                      'entrante']

        if not os.path.isdir('./cache'):
            try:
                os.mkdir("./cache")
            except OSError:
                print("Creation of the directory cache failed")
        fichier = open('./cache/' + mot_tmp + '_' + type_relation_tmp + '.pkl', "wb")
        pickle.dump(relations, fichier)
        fichier.close()
        return relations

    if cache == 0:
        return sans_cache(mot, type_relation)
    elif cache == 1 and (
            not os.path.isdir('./cache') or not os.path.isfile('./cache/' + mot + '_' + type_relation + '.pkl')):
        return sans_cache(mot, type_relation)
    elif cache == 1:
        fichier = open('./cache/' + mot + '_' + type_relation + '.pkl', "rb")
        relations = pickle.load(fichier)
        print(relations)
        print(type(relations))
        fichier.close()
        return relations
    else:
        sys.exit("cache doit etre egal a 0 ou 1")
