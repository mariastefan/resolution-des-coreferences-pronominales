import sys

sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import mot

if __name__ == '__main__':
    le_mot = 'bfjhjnfkfjiez'
    extraction_html = mot.extraction_html(le_mot, 'all')
    if extraction_html is not None:
        sys.exit('Problème de gestion de mots inexistants sur jdm ( dans extraction_mot.extraction_html() )\n'
                 'Le mot \'' + le_mot + '\' n\'est pas censé exister sur jdm mais la fonction ne retourne pas None !')
