import sys
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte

if __name__ == '__main__':
    # phrase = "L'humain a été mordu par le chien. Il lui a déchiré le bras. Il va ainsi retenir la leçon."
    # phrase = "Le chien est tombé dans le puits. Il s'est cassé le museau. Il va ainsi retenir la leçon."
    # phrase = "Le chien est tombé dans le puits. Il est profond."
    # phrase = "L'humain a mis un coup de poing au chien. Il lui a cassé le museau."
    # phrase = '\"Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.\"'
    # phrase = 'Le chien est tombé dans le puits. Il s\'est cassé le museau. Il n\'y a aucune raison de paniquer.'
    # phrase = 'Le chien est tombé dans le puits. Il s\'est cassé le museau. Il n\'y a aucune raison de paniquer.'
    # phrase = 'Adrien est tombé dans le puits. Il est maladroit celui-là.'
    # phrase = 'Adrien est tombé et a pleuré car Julien l\'a poussé. Il est méchant celui-là.'
    phrase = "Adrien est tombé car Julien a crié. Il est méchant celui-là."

    infos = analyses_texte.informations_pronoms(phrase)
    print(phrase)
    for pronom in infos:
        print(pronom)


