import os
import sys
sys.path.append(".")
from resolution_coreferences_pronominales import extraction_mot


if __name__ == '__main__':
    mot = 'être vivant'
    extraction_mot.relations_mot(mot, 'all', True)
    chemin = os.path.dirname(os.path.abspath(__file__)).split('/tests')[0]
    chemin_fichier = os.path.join(chemin, 'cache', extraction_mot.mot_sans_espaces(mot) + '_' + 'all' + '.pkl')
    if os.path.isfile(chemin_fichier):
        print('Le fichier\n' + chemin_fichier + '\na bien été créé (ou existait déjà)')
    else:
        print('Erreur création fichier ' + chemin_fichier)