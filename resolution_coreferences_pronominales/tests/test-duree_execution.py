import pandas as pd
from datetime import datetime
from resolution_coreferences_pronominales import extraction_mot
from resolution_coreferences_pronominales import traitements_phrase
import os
import time

if __name__ == '__main__':
    # Chemin du fichier où on sauvegarde les durées d'exécution
    chemin_fichier = os.path.dirname(os.path.dirname(__file__)) + "/data/historique_duree_execution.csv"

    # Initialisation DataFrame historique_duree_execution
    historique_duree_execution = ''
    if not os.path.isfile(chemin_fichier):
        historique_duree_execution = pd.DataFrame({'cache': [],
                                                   'extraction_mot.extraction_html()': [],
                                                   'difference_1': [],
                                                   'extraction_mot.relations_mot()': [],
                                                   'difference_2': [],
                                                   'extraction_mot.relations_entre_mots()': [],
                                                   'difference_3': [],
                                                   'traitements_phrase.informations_pronoms()': [],
                                                   'difference_4': [],
                                                   'traitements_phrase.coreferences_phrase()': [],
                                                   'difference_5': [],
                                                   'date': [],
                                                   'heure': [],
                                                   'mot': [],
                                                   'liste_mots': [],
                                                   'phrase': []
                                                   })
    else:
        historique_duree_execution = pd.read_csv(chemin_fichier)

    # Variables pour l'execution des fonctions
    mot = 'manger'
    liste_mots = ['chien', 'canaille', 'caniche', 'aboyer', 'être vivant', 'museau']
    phrase = 'Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.'
    nombre_repetitions_global = 1  # Attention ! nombre de boucles * 2. Ne pas mettre un nombre trop grand !
    nombre_repetitions_fonctions = 3  # ATTENTION ! CHAQUE fonction est appelée AUTANT de fois que ce nombre


    for i in range(nombre_repetitions_global * 2):
        cache = ''
        pourcentage_1 = ''
        pourcentage_2 = ''
        pourcentage_3 = ''
        pourcentage_4 = ''
        pourcentage_5 = ''

        if i % 2 == 0:
            cache = False
        else:
            cache = True

        ancienne_duree = historique_duree_execution.tail(2).reset_index(drop=True)
        # Calcul temps d'execution des differentes fonctions
        print('Debut calcul durée d\'execution extraction_mot.extraction_html')
        temps_execution_1 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            time.sleep(1)
            extraction_mot.extraction_html(mot, 'all')
            temps_execution_1 = (time.time() - start) + temps_execution_1
        temps_execution_1 = temps_execution_1 / nombre_repetitions_fonctions
        print('Fin calcul durée d\'execution extraction_mot.extraction_html')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution.empty:
            if temps_execution_1 > historique_duree_execution[
                historique_duree_execution['cache'] == cache
            ]['extraction_mot.extraction_html()'].max():
                print('\033[93m' + 'Attention ! Vérifiez extraction_mot.extraction_html() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if (not ancienne_duree.empty) and ancienne_duree.shape[0] > 1:
            pourcentage_1 = -1 * (
                    100 - ((100 * temps_execution_1) / ancienne_duree['extraction_mot.extraction_html()'][0]))
            if pourcentage_1 > 0:
                pourcentage_1 = '+' + str(round(pourcentage_1, 2)) + '%'
            else:
                pourcentage_1 = str(round(pourcentage_1, 2)) + '%'

        print('Debut calcul durée d\'execution extraction_mot.relations_mot')
        temps_execution_2 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            extraction_mot.relations_mot(mot, 'all', cache)
            temps_execution_2 = (time.time() - start) + temps_execution_2
        temps_execution_2 = temps_execution_2 / nombre_repetitions_fonctions
        print('Fin calcul durée d\'execution extraction_mot.relations_mot')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution.empty:
            if temps_execution_2 > historique_duree_execution[
                historique_duree_execution['cache'] == cache
            ]['extraction_mot.relations_mot()'].max():
                print('\033[93m' + 'Attention ! Vérifiez extraction_mot.relations_mot() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if (not ancienne_duree.empty) and ancienne_duree.shape[0] > 1:
            pourcentage_2 = -1 * (
                    100 - ((100 * temps_execution_2) / ancienne_duree['extraction_mot.relations_mot()'][0]))
            if pourcentage_2 > 0:
                pourcentage_2 = '+' + str(round(pourcentage_2, 2)) + '%'
            else:
                pourcentage_2 = str(round(pourcentage_2, 2)) + '%'

        print('Debut calcul durée d\'execution extraction_mot.relations_entre_mots')
        temps_execution_3 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            extraction_mot.relations_entre_mots(liste_mots, cache)
            temps_execution_3 = (time.time() - start) + temps_execution_3
        temps_execution_3 = temps_execution_3 / nombre_repetitions_fonctions
        print('Fin calcul durée d\'execution extraction_mot.relations_entre_mots')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution.empty:
            if temps_execution_3 > historique_duree_execution[
                historique_duree_execution['cache'] == cache
            ]['extraction_mot.relations_entre_mots()'].max():
                print('\033[93m' + 'Attention ! Vérifiez extraction_mot.relations_entre_mots() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if (not ancienne_duree.empty) and ancienne_duree.shape[0] > 1:
            pourcentage_3 = -1 * (100 - (
                    (100 * temps_execution_3) / ancienne_duree['extraction_mot.relations_entre_mots()'][0]))
            if pourcentage_3 > 0:
                pourcentage_3 = '+' + str(round(pourcentage_3, 2)) + '%'
            else:
                pourcentage_3 = str(round(pourcentage_3, 2)) + '%'

        print('Debut calcul durée d\'execution traitements_phrase.informations_pronoms')
        temps_execution_4 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            traitements_phrase.informations_pronoms(phrase)
            temps_execution_4 = (time.time() - start) + temps_execution_4
        temps_execution_4 = temps_execution_4 / nombre_repetitions_fonctions
        print('Fin calcul durée d\'execution traitements_phrase.informations_pronoms')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution.empty:
            if temps_execution_4 > historique_duree_execution[
                historique_duree_execution['cache'] == cache
            ]['traitements_phrase.informations_pronoms()'].max():
                print('\033[93m' + 'Attention ! Vérifiez traitements_phrase.informations_pronoms() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if (not ancienne_duree.empty) and ancienne_duree.shape[0] > 1:
            pourcentage_4 = -1 * (100 - (
                    (100 * temps_execution_4) / ancienne_duree['traitements_phrase.informations_pronoms()'][0]))
            if pourcentage_4 > 0:
                pourcentage_4 = '+' + str(round(pourcentage_4, 2)) + '%'
            else:
                pourcentage_4 = str(round(pourcentage_4, 2)) + '%'

        print('Debut calcul durée d\'execution traitements_phrase.coreferences_phrase')
        temps_execution_5 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            traitements_phrase.coreferences_phrase(phrase, cache)
            temps_execution_5 = (time.time() - start) + temps_execution_5
        temps_execution_5 = temps_execution_5 / nombre_repetitions_fonctions
        print('Fin calcul durée d\'execution traitements_phrase.coreferences_phrase')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution.empty:
            if temps_execution_5 > historique_duree_execution[
                historique_duree_execution['cache'] == cache
            ]['traitements_phrase.coreferences_phrase()'].max():
                print('\033[93m' + 'Attention ! Vérifiez traitements_phrase.coreferences_phrase() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if (not ancienne_duree.empty) and ancienne_duree.shape[0] > 1:
            pourcentage_5 = -1 * (100 - (
                    (100 * temps_execution_5) / ancienne_duree['traitements_phrase.coreferences_phrase()'][0]))
            if pourcentage_5 > 0:
                pourcentage_5 = '+' + str(round(pourcentage_5, 2)) + '%'
            else:
                pourcentage_5 = str(round(pourcentage_5, 2)) + '%'

        date = datetime.now().strftime("%d/%m/%Y")
        heure = datetime.now().strftime("%H:%M:%S")

        # Remplissage de historique_duree_execution avec les temps d'exécution, la date et l'heure actuelles
        historique_duree_execution = historique_duree_execution.append(
            pd.DataFrame(
                [[
                    cache,
                    temps_execution_1,
                    pourcentage_1,
                    temps_execution_2,
                    pourcentage_2,
                    temps_execution_3,
                    pourcentage_3,
                    temps_execution_4,
                    pourcentage_4,
                    temps_execution_5,
                    pourcentage_5,
                    date,
                    heure,
                    mot,
                    liste_mots,
                    phrase
                ]], columns=list(['cache',
                                  'extraction_mot.extraction_html()',
                                  'difference_1',
                                  'extraction_mot.relations_mot()',
                                  'difference_2',
                                  'extraction_mot.relations_entre_mots()',
                                  'difference_3',
                                  'traitements_phrase.informations_pronoms()',
                                  'difference_4',
                                  'traitements_phrase.coreferences_phrase()',
                                  'difference_5',
                                  'date',
                                  'heure',
                                  'mot',
                                  'liste_mots',
                                  'phrase'
                                  ])
            )
        )
        historique_duree_execution.to_csv(chemin_fichier, index=False)
