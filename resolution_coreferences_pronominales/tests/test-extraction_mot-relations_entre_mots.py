import sys
sys.path.append(".")
from resolution_coreferences_pronominales import extraction_mot

if __name__ == '__main__':
    cache = True
    liste_mots = ["eau", "rivière", "profond"]
    print("Résultat de extraction_mot.relations_entre_mots(" + str(liste_mots) + ", " + str(cache) + ") :")
    for e in extraction_mot.relations_entre_mots(liste_mots, True):
        print(e)

    liste_mots = ["eau", "rivièreeeee", "profond"]
    print("\nRésultat de extraction_mot.relations_entre_mots(" + str(liste_mots) + ", " + str(cache) + ") :")
    for e in extraction_mot.relations_entre_mots(liste_mots, True):
        print(e)
