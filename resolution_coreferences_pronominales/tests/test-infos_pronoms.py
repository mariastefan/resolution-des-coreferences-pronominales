import traitements_phrase

if __name__ == '__main__':
    phrase_tmp = "Le chien est tombé dans le puits. Il s'est cassé le museau. Il va ainsi retenir la leçon."
    # phrase_tmp = "Le chien est tombé dans le puits. Il est profond."
    infos = traitements_phrase.informations_pronoms(phrase_tmp)
    print(phrase_tmp)
    for pronom in infos:
        print(pronom)
