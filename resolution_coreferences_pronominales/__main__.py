import re

import extraction_mot
import time
import os

if __name__ == '__main__':
    # Paramètres à choisir :
    mot = 'amour'
    cache = 0
    relation = 'all'
    nb_boucle = 1

    relations_mot = {}
    time1 = 0
    start_time_total = time.time()
    for i in range(nb_boucle):
        start_time = time.time()
        relations_mot = extraction_mot.relations_mot(mot, relation, cache)
        time1 += time.time() - start_time
    # Pour print relations_mot :
    # for rid in relations_mot.keys():
    #     print(rid + " : " + str(relations_mot[rid]))
    # Imprime la durée d'exécution de extraction_mot.relations_mot (en moyenne)
    print("relations_mot --- %s seconds --- par boucle en moyenne" % (time1 / nb_boucle))
    print("temps total --- " + str((time.time() - start_time_total)) + " secondes ---, " + str(nb_boucle) + " boucle")
    print("Il y a " + str(len(relations_mot)) + " entrées dans relations_mot")
