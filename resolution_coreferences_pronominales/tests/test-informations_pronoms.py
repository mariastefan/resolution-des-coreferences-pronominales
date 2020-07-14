import sys
import os
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte


filename = os.path.basename(__file__)
print('Start : ' + filename)
phrase = "Le chien est tombé dans le puits. Il s'est cassé le museau. Il va ainsi retenir la leçon."
resultat = analyses_texte.informations_pronoms(phrase)
attendu = [
    ['Il', ['chien', 'puits'], {'ROOT': 'casser', 'sens': 'sortante', 'obj': 'museau'}],
    ["s'", ['chien', 'puits'], {'ROOT': 'casser', 'sens': 'sortante', 'obj': 'museau'}],
    ['Il', ['chien', 'puits', 'museau'], {'ROOT': 'aller', 'sens': 'sortante',
                                          'xcomp': ['retenir', {'aux': 'ainsi', 'obj': 'leçon'}]}]
]
try:
    assert resultat == attendu
except AssertionError:
    sys.exit(filename + ' FAILED for : ' + phrase)
print('Completed : ' + filename)

