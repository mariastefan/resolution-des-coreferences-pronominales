import sys
sys.path.append(".")
from resolution_coreferences_pronominales import extraction_mot

if __name__ == '__main__':
    mot = 'bfjhjnfkfjiez'
    extraction_html = extraction_mot.extraction_html(mot, 'all')
    if extraction_html is not None:
        sys.exit('Problème de gestion de mots inexistants sur jdm ( dans extraction_mot.extraction_html() )\n'
                 'Le mot \'' + mot + '\' n\'est pas censé exister sur jdm mais la fonction ne retourne pas None !')
