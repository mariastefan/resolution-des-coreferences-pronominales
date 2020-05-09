import extraction_mot
import coreferences_phrase

if __name__ == '__main__':
    liste_mots = ['chien', 'puits', 'museau']
    print('Voici les relations entre ' + str(liste_mots) + ' extraites grace à extraction_mot.relations_entre_mots([\'chien\', \'puits\', \'museau\'], True)')
    for e in extraction_mot.relations_entre_mots(liste_mots, True):
        print(e)
    phrase_tmp = '\"Le chien est tombé dans le puits. Il s\'est cassé le museau. Il va ainsi retenir la leçon.\"'
    infos = coreferences_phrase.infos_pronoms(phrase_tmp)
    print('\nLa phrase et les informations sur ses pronoms :')
    print(phrase_tmp)
    for pronom in infos:
        print(pronom)

    print('\nMaintenant il faut trouver les coréférences des pronoms grace à ces informations.')
