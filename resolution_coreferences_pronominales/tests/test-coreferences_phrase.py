import coreferences_phrase

if __name__ == '__main__':
    phrase_tmp = "Le chien est tombé dans le puits. Il s'est cassé le museau. Il va ainsi retenir la leçon."
    # phrase_tmp = "Le chien est tombé dans le puits. Il est profond."
    infos = coreferences_phrase.infos_pronoms(phrase_tmp)
    print(phrase_tmp)
    for pronom in infos:
        print(pronom)
