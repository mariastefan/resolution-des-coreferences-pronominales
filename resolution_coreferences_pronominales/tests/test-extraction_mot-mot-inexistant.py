import sys
import os

sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import mot

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print('Start : ' + filename)
    le_mot = 'bfjhjnfkfjiez'
    extraction_html = mot.extraction_html(le_mot, 'all')
    try:
        assert extraction_html is None
    except AssertionError:
        sys.exit(filename + ' : Problème de gestion de mots inexistants sur jdm ( '
                            'dans extraction_mot.extraction_html() )\n'
                            'Le mot \'' + le_mot + '\' n\'est pas censé exister sur jdm mais la fonction ne '
                                                   'retourne pas None !')
    print('Completed : ' + filename)
