import traitements_phrase

if __name__ == '__main__':
    # phrase = "Le chien est tombé dans le puits. Il s'est cassé le museau. Il va ainsi retenir la leçon."
    # phrase = "Le chien a été blessé par le puits. Il s'est cassé le museau. " \
    # phrase = "Il sera comblé avant qu'il ne se blesse encore. "
    phrase = "L'humain a mis un coup de poing au chien. Il lui a cassé le museau."
    # phrase = "Le chat est tombé dans le puits. Il est profond. Il s'est blessé la pate."
    print(phrase)

    # print(traitements_phrase.informations_pronoms(phrase))
    # print(traitements_phrase.coreferences_phrase(phrase, True))
    print(traitements_phrase.affichier_antecedents_dans_phrase(phrase, True))
