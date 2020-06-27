import sys

sys.path.append(".")

from resolution_coreferences_pronominales.coreferences import mot

if __name__ == '__main__':
    cache = True
    le_mot = 'chatouilles'
    for e in mot.relations_mot(le_mot, 'all', False):
        print(e)
