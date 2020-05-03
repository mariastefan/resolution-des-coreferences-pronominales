import re
import pandas as pd
from bs4 import BeautifulSoup
import requests


# Fonction permettant l'insertion du mot rq_word dans l'URL lors de la requete à jdm
# Appelée seulement dans extraction_html
def conversion_mot(rq_word):
    conversion_partielle = rq_word.encode('iso-8859-1')
    resultat = re.search("b[\"'](.*)[\"']$", str(conversion_partielle))
    resultat = resultat.group(1)
    resultat = resultat.replace("'", '%27')
    resultat = resultat.replace('\\x', '%')
    return resultat


# Prend rq_word (mot recherché) et retourne le code html correspondant depuis http://www.jeuxdemots.org/rezo-dump
def extraction_html(rq_word, type_relation):
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
def creation_tab_relations(mot, type_relation):
    texte_brut = extraction_html(mot, type_relation)
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

    return relations
