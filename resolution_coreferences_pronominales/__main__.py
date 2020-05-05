import extraction_mot
import time

if __name__ == '__main__':
    time1 = 0
    time2 = 0
    nb_boucle = 5
    start_time_total = time.time()
    for i in range(nb_boucle):
        start_time = time.time()
        extraction_mot.old_relations_mot('puits', 'all', 0)
        time1 += time.time() - start_time
        start_time = time.time()
        extraction_mot.relations_mot('puits', 'all', 0)
        time2 += time.time() - start_time
    print("old_relations_mot --- %s seconds --- par boucle en moyenne" % (time1/nb_boucle))
    print("relations_mot --- %s seconds --- par boucle en moyenne" % (time2/nb_boucle))
    print("temps total --- "+str((time.time() - start_time_total))+" secondes ---, "+str(nb_boucle)+" fois")
