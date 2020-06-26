import sys
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences.relations_entre_mots import relations_entre_mots

if __name__ == '__main__':
    cache = True
    liste_mots = ["eau", "rivière", "profond"]
    print("Résultat de relations_entre_mots(" + str(liste_mots) + ", " + str(cache) + ") :")
    for e in relations_entre_mots(liste_mots, True):
        print(e)

    liste_mots = ["eau", "rivièreeeee", "profond"]
    print("\nRésultat de relations_entre_mots(" + str(liste_mots) + ", " + str(cache) + ") :")
    for e in relations_entre_mots(liste_mots, True):
        print(e)
