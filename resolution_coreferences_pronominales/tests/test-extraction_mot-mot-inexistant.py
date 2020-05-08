import extraction_mot

if __name__ == '__main__':
    # Paramètres à choisir :
    mot = 'adsqmour'

    relations_mot = extraction_mot.relations_mot(mot, 'all', 0)
    if relations_mot is None:
        print("Le mot " + mot + " n'existe pas sur jeuxdemots.org !")
    else:
        print("Il y a " + str(len(relations_mot)) + " entrées dans relations_mot")
    extraction_mot.supprimer_cache()
