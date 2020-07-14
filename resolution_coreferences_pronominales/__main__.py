import sys
import os

sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print('Start ' + filename)
    phrase = "Le chat est tombé dans le puits. Il est profond. Il s'est blessé la patte."
    print(phrase)
    print("\nChargement en cours... \n")
    print(analyses_texte.affichier_antecedents_dans_phrase(phrase, True))
    print('Completed : ' + filename)
