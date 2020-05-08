import extraction_mot
import time

if __name__ == '__main__':
    # Paramètres à choisir :
    mot = 'chien'
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

    # Imprime la durée d'exécution de extraction_mot.relations_mot (en moyenne)
    print("relations_mot(" + mot + ", " + relation + ", " + str(cache) + " --- " + str(
        (time1 / nb_boucle)) + " secondes --- par boucle en moyenne")
    print("temps total --- " + str((time.time() - start_time_total)) + " secondes --- pour " + str(
        nb_boucle) + " boucles")

    # Si vous voulez vider le cache :
    # extraction_mot.vider_cache()
