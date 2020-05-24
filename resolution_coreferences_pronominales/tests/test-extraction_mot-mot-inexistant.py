import sys
sys.path.append(".")
from resolution_coreferences_pronominales import extraction_mot

if __name__ == '__main__':
    # Paramètres à choisir :
    mot = 'adsqmour'
    relations_mot = extraction_mot.relations_mot(mot, 'all', False)
    if relations_mot is not None:
        print("Il y a " + str(len(relations_mot)) + " entrées dans relations_mot")
