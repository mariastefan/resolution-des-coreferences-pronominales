import extraction_mot

if __name__ == '__main__':
    liste_mots = ["eau", "rivière", "profond"]
    print("Résultat de extraction_mot.relations_entre_mots(" + str(liste_mots) + ", True) :")
    for e in extraction_mot.relations_entre_mots(liste_mots, True):
        print(e)

    liste_mots = ["eau", "rivièreeeee", "profond"]
    print("\nRésultat de extraction_mot.relations_entre_mots(" + str(liste_mots) + ", True) :")
    for e in extraction_mot.relations_entre_mots(liste_mots, True):
        print(e)
