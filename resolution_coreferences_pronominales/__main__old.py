import extraction_mot_old
import time
import pandas as pd
import re
import os

if __name__ == '__main__':
    mot = 'manger'
    cache = 1
    relation = 'all'
    nb_boucle = 1

    time1 = 0
    time2 = 0
    # res1 = {}
    res2 = {}
    # res1 = pd.DataFrame(
    #         columns=('id_relation', 'lautre_noeud', 'type_relation', 'poids_relation', 'sens_relation'))
    start_time_total = time.time()
    for i in range(nb_boucle):
        # start_time = time.time()
        # # res1 = extraction_mot_old.old_relations_mot(mot, relation, cache)
        # time1 += time.time() - start_time
        start_time = time.time()
        res2 = extraction_mot_old.relations_mot(mot, relation, cache)
        time2 += time.time() - start_time
    # print("old_relations_mot --- %s seconds --- par boucle en moyenne" % (time1/nb_boucle))
    print("relations_mot --- %s seconds --- par boucle en moyenne" % (time2/nb_boucle))
    print("temps total --- "+str((time.time() - start_time_total))+" secondes ---, "+str(nb_boucle)+" fois")
    # print(res1.shape)
    # for key in res2.keys():
    #     print(key + ' : '+str(res2[key]))
    # print(res2)
    print(len(res2))
    # a = []
    # f = open("puits", "r")
    # count = 0
    # for x in f:
    #     res = re.search("r;([0-9]*);.*", x)
    #     if res:
    #         a.append(res.group(1))
    #     count +=1
    # print(len(a))
    # print(count)

