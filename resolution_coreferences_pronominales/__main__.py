import sys
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte

if __name__ == '__main__':
    phrase = "Le chat est tombé dans le puits. Il est profond. Il s'est blessé la patte."
    print(phrase)
    print("\nChargement en cours... \n")
    infos = analyses_texte.informations_pronoms(phrase)
    print(analyses_texte.affichier_antecedents_dans_phrase(phrase, True))
    print('\nRésultat de la fonction analyses_texte.informations_pronoms(phrase) :')
    print(analyses_texte.informations_pronoms(phrase))


