import extraction_mot
import traitements_phrase

if __name__ == '__main__':
    phrase = "Le chat est tombé dans le puits. Il est profond. Il s'est blessé la pate."
    infos = traitements_phrase.informations_pronoms(phrase)
    print(phrase)
    print("\nChargement en cours... \n")
    print(traitements_phrase.affichier_antecedents_dans_phrase(phrase, True))
    print('\nRésultat de la fonction traitements_phrase.informations_pronoms(phrase) :')
    print(traitements_phrase.informations_pronoms(phrase))


