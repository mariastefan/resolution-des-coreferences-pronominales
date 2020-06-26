import pandas as pd
from datetime import datetime
import sys

sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte
from resolution_coreferences_pronominales.coreferences import mot
from resolution_coreferences_pronominales.coreferences.relations_entre_mots import relations_entre_mots
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
# contenues dans mot.py et analyses_texte.py.
# Chaque fonction est testée nombre_repetitions_fonctions fois. La mediane du temps d'execution est gardée pour chacune.
# On ajoute aussi la difference, en pourcentage, entre chaque durée d'exécution et la mediane des
# durées précédentes (difference_1, difference_2, ...)
# voir data/historique_duree_execution.csv pour plus d'informations

if __name__ == '__main__':
    # Variables pour l'execution des fonctions
    le_mot = 'manger'
    liste_mots = ['chien', 'canaille', 'caniche', 'aboyer', 'être vivant', 'museau']
    phrase = 'Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.'

    # Le script prend deux paramètres :
    if len(sys.argv) != 3:
        sys.exit('Attention ! test-duree_execution.py necessite deux paramètres (dans cet ordre) :\n'
                 '\033[1m\033[95mnombre_repetitions_global\033[0m => nombre de fois que le script s\'exécute\n'
                 '\033[1m\033[95mnombre_repetitions_fonctions\033[0m => nombre de fois que CHAQUE FONCTION est executée (pour une meilleure '
                 'estimation du temps d\'execution c\'est mieux de les executer plus d\'une fois.)\n')
    try:
        nombre_repetitions_global = int(
            sys.argv[1])  # le nombre de repets est * 2. Ne pas mettre un nombre trop grand !
        nombre_repetitions_fonctions = int(sys.argv[2])  # CHAQUE fonction est appelée AUTANT de fois que ce nombre
    except ValueError:
        sys.exit('Attention, un des deux premiers paramètres n\'est pas un entier !\n'
                 'Paramètres (dans cet ordre) :\n'
                 '\033[1m\033[95mnombre_repetitions_global\033[0m => nombre de fois que le script s\'exécute\n'
                 '\033[1m\033[95mnombre_repetitions_fonctions\033[0m => nombre de fois que CHAQUE FONCTION est executée (pour une meilleure '
                 'estimation du temps d\'execution c\'est mieux de les executer plus d\'une fois.)\n')

    # Chemin du fichier où on sauvegarde les durées d'exécution
    chemin_fichier = "historique_duree_execution.csv"

    # Initialisation DataFrame historique_duree_execution
    historique_duree_execution = ''
    if not os.path.isfile(chemin_fichier):
        historique_duree_execution = pd.DataFrame({'cache': [],
                                                   'nb_reps_fcts': [],
                                                   'mot.extraction_html()': [],
                                                   'difference_1': [],
                                                   'mot.relations_mot()': [],
                                                   'difference_2': [],
                                                   'relations_entre_mots()': [],
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
        # print('Debut calcul durée d\'execution mot.extraction_html')
        temps_execution_1 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            mot.extraction_html(le_mot, 'all')
            temps_execution_1 = (time.time() - start) + temps_execution_1
        temps_execution_1 = temps_execution_1 / nombre_repetitions_fonctions
        print('Fin 1 : mot.extraction_html')

        # On vérifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_1 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['mot.extraction_html()'].max():
                print('\033[93m' + 'Attention ! Vérifiez mot.extraction_html() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            # On calcule la mediane des précedentes durées d'exécution
            mediane_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                'mot.extraction_html()'].median()

            # pourcentage_1 correspond à la différence en pourcentage entre le nouveau temps d'exécution de la fonction
            # 1 et la mediane des anciens temps d'exécution dans le fichier de la fonction 1
            pourcentage_1 = -1 * (
                    100 - ((100 * temps_execution_1) / mediane_duree_precedents))

            if pourcentage_1 > 0:
                pourcentage_1 = '+' + str(round(pourcentage_1, 2)) + '%'
            else:
                pourcentage_1 = str(round(pourcentage_1, 2)) + '%'

        # print('Debut calcul durée d\'execution mot.relations_mot')
        temps_execution_2 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            mot.relations_mot(le_mot, 'all', cache)
            temps_execution_2 = (time.time() - start) + temps_execution_2
        temps_execution_2 = temps_execution_2 / nombre_repetitions_fonctions
        print('Fin 2 : mot.relations_mot')

        # On vérifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_2 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['mot.relations_mot()'].max():
                print('\033[93m' + 'Attention ! Vérifiez mot.relations_mot() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            mediane_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                'mot.relations_mot()'].median()

            pourcentage_2 = -1 * (
                    100 - ((100 * temps_execution_2) / mediane_duree_precedents))

            if pourcentage_2 > 0:
                pourcentage_2 = '+' + str(round(pourcentage_2, 2)) + '%'
            else:
                pourcentage_2 = str(round(pourcentage_2, 2)) + '%'

        # print('Debut calcul durée d\'execution relations_entre_mots')
        temps_execution_3 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            relations_entre_mots(liste_mots, cache)
            temps_execution_3 = (time.time() - start) + temps_execution_3
        temps_execution_3 = temps_execution_3 / nombre_repetitions_fonctions
        print('Fin 3 : relations_entre_mots')

        # On verifie que la durée d'execution n'excède pas la plus grande présente dans le csv
        if not historique_duree_execution_old.empty:
            if temps_execution_3 > historique_duree_execution_old[
                historique_duree_execution_old['cache'] == cache
            ]['relations_entre_mots()'].max():
                print('\033[93m' + 'Attention ! Vérifiez relations_entre_mots() ! '
                                   'Sa durée d\'exécution parait anormale' + '\033[0m')

        if not ancienne_duree.empty:
            mediane_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                'relations_entre_mots()'].median()

            pourcentage_3 = -1 * (
                    100 - ((100 * temps_execution_3) / mediane_duree_precedents))
            if pourcentage_3 > 0:
                pourcentage_3 = '+' + str(round(pourcentage_3, 2)) + '%'
            else:
                pourcentage_3 = str(round(pourcentage_3, 2)) + '%'

        # print('Debut calcul durée d\'execution traitements_phrase.informations_pronoms')
        temps_execution_4 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            analyses_texte.informations_pronoms(phrase)
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
            mediane_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                'traitements_phrase.informations_pronoms()'].median()

            pourcentage_4 = -1 * (
                    100 - ((100 * temps_execution_4) / mediane_duree_precedents))

            if pourcentage_4 > 0:
                pourcentage_4 = '+' + str(round(pourcentage_4, 2)) + '%'
            else:
                pourcentage_4 = str(round(pourcentage_4, 2)) + '%'

        # print('Debut calcul durée d\'execution traitements_phrase.coreferences_phrase')
        temps_execution_5 = 0
        for j in range(nombre_repetitions_fonctions):
            start = time.time()
            analyses_texte.coreferences_phrase(phrase, cache)
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
            mediane_duree_precedents = historique_duree_execution_old[historique_duree_execution_old['cache'] == cache][
                'traitements_phrase.coreferences_phrase()'].median()

            pourcentage_5 = -1 * (
                    100 - ((100 * temps_execution_5) / mediane_duree_precedents))

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
                    nombre_repetitions_fonctions,
                    round(temps_execution_1, 3),
                    pourcentage_1,
                    round(temps_execution_2, 3),
                    pourcentage_2,
                    round(temps_execution_3, 3),
                    pourcentage_3,
                    round(temps_execution_4, 3),
                    pourcentage_4,
                    round(temps_execution_5, 3),
                    pourcentage_5,
                    date,
                    heure,
                    le_mot,
                    liste_mots,
                    phrase
                ]], columns=list(['cache',
                                  'nb_reps_fcts',
                                  'mot.extraction_html()',
                                  'difference_1',
                                  'mot.relations_mot()',
                                  'difference_2',
                                  'relations_entre_mots()',
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
