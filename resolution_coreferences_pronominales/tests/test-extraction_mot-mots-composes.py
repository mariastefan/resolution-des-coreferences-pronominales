import os
import sys

sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import mot

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print('Start : ' + filename)
    le_mot = 'être vivant'
    mot.relations_mot(le_mot, 'all', True)
    if ' ' in le_mot:
        mot_sans_espaces = le_mot.replace(' ', '_')
    chemin = os.path.dirname(os.path.abspath(__file__)).split('/tests')[0]
    chemin_fichier = os.path.join(chemin, 'cache', mot_sans_espaces + '_' + 'all' + '.pkl')
    if os.path.isfile(chemin_fichier):
        print('Le fichier\n' + chemin_fichier + '\na bien été créé (ou existait déjà)')
    else:
        print(filename + ' : Erreur création fichier ' + chemin_fichier)
    print('Completed : ' + filename)
