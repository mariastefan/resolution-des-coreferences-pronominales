import pandas as pd
from datetime import datetime
import sys

sys.path.append(".")
from resolution_coreferences_pronominales import extraction_mot
from resolution_coreferences_pronominales import traitements_phrase
import os
import time

# python3 test-duree_execution.py nombre_repetitions_global nombre_repetitions_fonctions

# nombre_repetitions_global => nombre de fois que le script s'exécute
# nombre_repetitions_fonctions => nombre de fois que CHAQUE FONCTION est executée (pour une meilleure estimation du
# temps d'execution c'est mieux de les executer plus d'une fois.)

# Ce programme remplit le fichier data/historique_duree_execution.csv
# Le but du programme est de sauvegarder le temps d'execution des fonctions du
# projet afin de détecter les ralentissements (modifications, ...)
# Ce programme execute nombre_repetitions_global fois les fonctions principales du projet,
# contenues dans extraction_mot.py et traitements_phrase.py.
# Chaque fonction est testée nombre_repetitions_fonctions fois. La moyenne du temps d'execution est gardée pour chacune.
# On ajoute aussi la difference, en pourcentage, entre chaque durée d'exécution et la moyenne des
# durées précédentes (difference_1, difference_2, ...)
# voir data/historique_duree_execution.csv pour plus d'informations

if __name__ == '__main__':
    # Variables pour l'execution des fonctions
    mot = 'manger'
    liste_mots = ['chien', 'canaille', 'caniche', 'aboyer', 'être vivant', 'museau']
    phrase = 'Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.'

    # Le script prend deux paramètres :
    if len(sys.argv) != 4:
        sys.exit('Attention ! test-duree_execution.py necessite trois paramètres (dans cet ordre) :\n'
                 '\033[1m\033[95mnombre_repetitions_global\033[0m => nombre de fois que le script s\'exécute\n'
                 '\033[1m\033[95mnombre_repetitions_fonctions\033[0m => nombre de fois que CHAQUE FONCTION est executée (pour une meilleure '
                 'estimation du temps d\'execution c\'est mieux de les executer plus d\'une fois.)\n'
                 '\033[1m\033[95m-m\033[0m OU \033[1m\033[95m-d\033[0m => valeurs des colonnes difference_ calculées en fonction de la moyenne|dernier des '
                 'anciennes durées d\'execution des fonctions respectives')
    try:
        nombre_repetitions_global = int(
            sys.argv[1])  # le nombre de repets est * 2. Ne pas mettre un nombre trop grand !
        nombre_repetitions_fonctions = int(sys.argv[2])  # CHAQUE fonction est appelée AUTANT de fois que ce nombre
    except ValueError:
        sys.exit('Attention, un des deux premiers paramètres n\'est pas un entier !\n'
                 'Paramètres (dans cet ordre) :\n'
                 '\033[1m\033[95mnombre_repetitions_global\033[0m => nombre de fois que le script s\'exécute\n'
                 '\033[1m\033[95mnombre_repetitions_fonctions\033[0m => nombre de fois que CHAQUE FONCTION est executée (pour une meilleure '
                 'estimation du temps d\'execution c\'est mieux de les executer plus d\'une fois.)\n'
                 '\033[1m\033[95m-m\033[0m OU \033[1m\033[95m-d\033[0m => valeurs des colonnes difference_ calculées en fonction de la moyenne|dernier des '
                 'anciennes durées d\'execution des fonctions respectives')
    methode_calcul_pourcentage = sys.argv[3]
    if methode_calcul_pourcentage != '-m' and methode_calcul_pourcentage != '-d':
        sys.exit('Attention, le troisième paramètre doit etre' + '\033[1m\033[95m' + ' -m' +
                 '\033[0m' + ' ou ' + '\033[1m\033[95m' + '-d' + '\033[0m')

    # Chemin du fichier où on sauvegarde les durées d'exécution
    chemin_fichier = os.path.dirname(os.path.dirname(__file__)) + "/data/historique_duree_execution.csv"

    # Initialisation DataFrame historique_duree_execution
    historique_duree_execution = ''
    if not os.path.isfile(chemin_fichier):
        historique_duree_execution = pd.DataFrame({'cache': [],
                                                   'nb_reps_fcts': [],
                                                   'methode': [],
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

    # Si le nombre de lignes n'est pas pair cela veut dire qu'il y a eu une erreur lors de la dernière execution, on
    # efface alors la dernière ligne pour avoir un nombre pair de lignes
    if historique_duree_execution.shape[0] % 2 != 0:
        historique_duree_execution.drop(historique_duree_execution.tail(1).index, inplace=True)

    ancienne_duree_pas_cache = historique_duree_execution.tail(2).reset_index(drop=True)
    ancienne_duree_cache = historique_duree_execution.tail(2).reset_index(drop=True)
    if historique_duree_execution.tail(2).reset_index(drop=True).shape[0] == 2:
        ancienne_duree_pas_cache = historique_duree_execution.tail(2).reset_index(drop=True).loc[0]
        ancienne_duree_cache = historique_duree_execution.tail(2).reset_index(drop=True).loc[1]

    historique_duree_execution_old = historique_duree_execution

    # On boucle deux fois le tout pour exécuter les fonctions avec cache=False et cache=True
    for i in range(nombre_repetitions_global * 2):
        cache = ''
        pourcentage_1 = ''
        pourcentage_2 = ''
        pourcentage_3 = ''
        pourcentage_4 = ''
        pourcentage_5 = ''
        ancienne_duree = ''
        if i % 2 == 0:
            cache = False
            ancienne_duree = ancienne_duree_pas_cache
        else:
            ancienne_duree = ancienne_duree_cache
            cache = True

        # Calcul temps d'execution des differentes fonctions
        # print('Debut calcul durée d\'execution extraction_mot.extraction_html')
        temps_execution_1 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            extraction_mot.extraction_html(mot, 'all')
            temps_execution_1 = (time.time() - start) + temps_execution_1
        temps_execution_1 = temps_execution_1 / nombre_repetitions_fonctions
        print('Fin 1 : extraction_mot.extraction_html')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_1 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['extraction_mot.extraction_html()'].max():
                print('\033[93m' + 'Attention ! Vérifiez extraction_mot.extraction_html() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            if methode_calcul_pourcentage == '-m':
                moyenne_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                    'extraction_mot.extraction_html()'].mean()

                pourcentage_1 = -1 * (
                        100 - ((100 * temps_execution_1) / moyenne_duree_precedents))
            else:
                pourcentage_1 = -1 * (
                        100 - ((100 * temps_execution_1) / ancienne_duree['extraction_mot.extraction_html()'])
                )

            if pourcentage_1 > 0:
                pourcentage_1 = '+' + str(round(pourcentage_1, 2)) + '%'
            else:
                pourcentage_1 = str(round(pourcentage_1, 2)) + '%'

        # print('Debut calcul durée d\'execution extraction_mot.relations_mot')
        temps_execution_2 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            extraction_mot.relations_mot(mot, 'all', cache)
            temps_execution_2 = (time.time() - start) + temps_execution_2
        temps_execution_2 = temps_execution_2 / nombre_repetitions_fonctions
        print('Fin 2 : extraction_mot.relations_mot')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_2 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['extraction_mot.relations_mot()'].max():
                print('\033[93m' + 'Attention ! Vérifiez extraction_mot.relations_mot() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            if methode_calcul_pourcentage == '-m':
                moyenne_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                    'extraction_mot.relations_mot()'].mean()

                pourcentage_2 = -1 * (
                        100 - ((100 * temps_execution_2) / moyenne_duree_precedents))
            else:
                pourcentage_2 = -1 * (
                        100 - ((100 * temps_execution_2) / ancienne_duree['extraction_mot.relations_mot()'])
                )
            if pourcentage_2 > 0:
                pourcentage_2 = '+' + str(round(pourcentage_2, 2)) + '%'
            else:
                pourcentage_2 = str(round(pourcentage_2, 2)) + '%'

        # print('Debut calcul durée d\'execution extraction_mot.relations_entre_mots')
        temps_execution_3 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            extraction_mot.relations_entre_mots(liste_mots, cache)
            temps_execution_3 = (time.time() - start) + temps_execution_3
        temps_execution_3 = temps_execution_3 / nombre_repetitions_fonctions
        print('Fin 3 : extraction_mot.relations_entre_mots')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_3 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['extraction_mot.relations_entre_mots()'].max():
                print('\033[93m' + 'Attention ! Vérifiez extraction_mot.relations_entre_mots() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            if methode_calcul_pourcentage == '-m':
                moyenne_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                    'extraction_mot.relations_entre_mots()'].mean()

                pourcentage_3 = -1 * (
                        100 - ((100 * temps_execution_3) / moyenne_duree_precedents))
            else:
                pourcentage_3 = -1 * (
                        100 - ((100 * temps_execution_3) / ancienne_duree['extraction_mot.relations_entre_mots()'])
                )
            if pourcentage_3 > 0:
                pourcentage_3 = '+' + str(round(pourcentage_3, 2)) + '%'
            else:
                pourcentage_3 = str(round(pourcentage_3, 2)) + '%'

        # print('Debut calcul durée d\'execution traitements_phrase.informations_pronoms')
        temps_execution_4 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            traitements_phrase.informations_pronoms(phrase)
            temps_execution_4 = (time.time() - start) + temps_execution_4
        temps_execution_4 = temps_execution_4 / nombre_repetitions_fonctions
        print('Fin 4 : traitements_phrase.informations_pronoms')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_4 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['traitements_phrase.informations_pronoms()'].max():
                print('\033[93m' + 'Attention ! Vérifiez traitements_phrase.informations_pronoms() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            if methode_calcul_pourcentage == '-m':
                moyenne_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                    'traitements_phrase.informations_pronoms()'].mean()

                pourcentage_4 = -1 * (
                        100 - ((100 * temps_execution_4) / moyenne_duree_precedents))
            else:
                pourcentage_4 = -1 * (
                        100 - (
                        (100 * temps_execution_4) / ancienne_duree['traitements_phrase.informations_pronoms()'])
                )

            if pourcentage_4 > 0:
                pourcentage_4 = '+' + str(round(pourcentage_4, 2)) + '%'
            else:
                pourcentage_4 = str(round(pourcentage_4, 2)) + '%'

        # print('Debut calcul durée d\'execution traitements_phrase.coreferences_phrase')
        temps_execution_5 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            traitements_phrase.coreferences_phrase(phrase, cache)
            temps_execution_5 = (time.time() - start) + temps_execution_5
        temps_execution_5 = temps_execution_5 / nombre_repetitions_fonctions
        print('Fin 5 : traitements_phrase.coreferences_phrase')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_5 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['traitements_phrase.coreferences_phrase()'].max():
                print('\033[93m' + 'Attention ! Vérifiez traitements_phrase.coreferences_phrase() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            if methode_calcul_pourcentage == '-m':
                moyenne_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                    'traitements_phrase.coreferences_phrase()'].mean()

                pourcentage_5 = -1 * (
                        100 - ((100 * temps_execution_5) / moyenne_duree_precedents))
            else:
                pourcentage_5 = -1 * (
                        100 - (
                        (100 * temps_execution_5) / ancienne_duree['traitements_phrase.coreferences_phrase()'])
                )

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
                    round(cache, 0),
                    round(nombre_repetitions_fonctions, 0),
                    methode_calcul_pourcentage,
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
                                  'nb_reps_fcts',
                                  'methode',
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
        print('Ligne ajoutée dans historique_duree_execution.csv')
