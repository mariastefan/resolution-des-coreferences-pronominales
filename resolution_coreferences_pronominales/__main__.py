import extraction_mot
import traitements_phrase

if __name__ == '__main__':
    phrase = '\"Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.\"'
    infos = traitements_phrase.informations_pronoms(phrase)
    print(phrase)
    print("\nChargement en cours... \n")
    print(traitements_phrase.affichier_antecedents_dans_phrase(phrase, True))
    print('\nRésultat de la fonction traitements_phrase.informations_pronoms(phrase) :')
    print(traitements_phrase.informations_pronoms(phrase))


