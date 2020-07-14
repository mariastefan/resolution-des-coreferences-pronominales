import sys

sys.path.append(".")
import time
from resolution_coreferences_pronominales.coreferences import mot

if __name__ == '__main__':
    # Paramètres
    le_mot = 'chien'
    cache = False
    relation = 'all'
    nb_boucle = 1

    relations_mot = {}
    time1 = 0
    start_time_total = time.time()
    for i in range(nb_boucle):
        start_time = time.time()
        relations_mot = mot.relations_mot(le_mot, relation, cache)
        time1 += time.time() - start_time

    # Imprime la durée d'exécution d'extraction_mot.relations_mot (en moyenne)
    print("relations_mot(" + le_mot + ", " + relation + ", " + str(cache) + " --- " + str(
        (time1 / nb_boucle)) + " secondes --- par boucle en moyenne")
    print("temps total --- " + str((time.time() - start_time_total)) + " secondes --- pour " + str(
        nb_boucle) + " boucles")
