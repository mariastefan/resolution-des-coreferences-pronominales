import sys
import os
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences.relations_entre_mots import relations_entre_mots

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print('Start : ' + filename)
    cache = True
    liste_mots = ["eau", "rivière", "profond"]
    resultat = relations_entre_mots(liste_mots, cache)
    attendu = [
        ['eau', 'rivière',
         {0: 0.000423, 10: 0.000273, 15: 0.000606, 27: 2.7e-05, 35: 7.1e-05, 666: 4e-06, 163: 2.5e-05}],
        ['rivière', 'eau', {0: 0.000493, 3: 3.5e-05, 9: 7.1e-05, 10: -0.040313549832026875, 28: 0.000448, 50: 6.5e-05,
                            666: 4e-06, 131: 2.5e-05}],
        ['profond', 'eau', {0: 3.2e-05}]

    ]
    try:
        assert resultat == attendu
    except AssertionError:
        sys.exit('test-extraction_mot-relations_entre_mots.py FAILED for : ' + str(liste_mots))

    liste_mots = ["eau", "rivièreeeee", "profond"]
    resultat = relations_entre_mots(liste_mots, cache)
    attendu = [
        ['profond', 'eau', {0: 3.2e-05}]
    ]
    try:
        assert resultat == attendu
    except AssertionError:
        sys.exit(filename + ' FAILED for : ' + str(liste_mots))
    print('Completed : ' + filename)


