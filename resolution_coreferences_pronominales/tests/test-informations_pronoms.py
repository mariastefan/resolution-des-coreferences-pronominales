import traitements_phrase


if __name__ == '__main__':
    # phrase = "L'humain a été mordu par le chien. Il lui a déchiré le bras. Il va ainsi retenir la leçon."
    # phrase = "Le chien est tombé dans le puits. Il s'est cassé le museau. Il va ainsi retenir la leçon."
    # phrase = "Le chien est tombé dans le puits. Il est profond."
    # phrase = "L'humain a mis un coup de poing au chien. Il lui a cassé le museau."
    phrase = '\"Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.\"'

    infos = traitements_phrase.informations_pronoms(phrase)
    print(phrase)
    for pronom in infos:
        print(pronom)
    # print(antecedents_rel.antecedents_et_verbe_des_pronoms(phrase_tmp))
