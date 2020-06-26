import os
import sys

chemin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
chemin = chemin + '/cache/'


def set_chemin_cache(chemin_tmp: str):
    chemin = chemin_tmp


def get_chemin_cache():
    return chemin


def creer_fichier(mot: str, type_relation: str):
    if ' ' in mot:
        mot = mot.replace(' ', '_')
    chemin_fichier = chemin + mot + '_' + type_relation + '.pkl'
    try:
        fichier = open(chemin + mot + '_' + type_relation + '.pkl', 'wb')
    except Exception as e:
        sys.exit('Impossible de créer le fichier ' + chemin_fichier + '\nMotif : %s' % e)
    return fichier


def ouvrir_fichier(mot: str, type_relation: str, droits: str):
    if ' ' in mot:
        mot = mot.replace(' ', '_')
    chemin_fichier = chemin + mot + '_' + type_relation + '.pkl'
    if not existe() or not contient_fichier(mot, type_relation):
        print('Erreur ouverture du fichier ' + chemin_fichier)
        return None
    try:
        fichier = open(chemin + mot + '_' + type_relation + '.pkl', droits)
    except Exception as e:
        sys.exit('Impossible d\'ouvrir le fichier ' + chemin_fichier + '\nMotif : %s' % e)
    return fichier


def fermer_fichier(fichier):
    try:
        fichier.close()
    except Exception as e:
        print('Impossible de fermer le fichier ' + fichier + '\nMotif : %s' % e + ' Le programme continue.')
        pass


def existe():
    return os.path.isdir(chemin)


def contient_fichier(mot: str, type_relation: str):
    if ' ' in mot:
        mot = mot.replace(' ', '_')
    return os.path.isfile(chemin + mot + '_' + type_relation + '.pkl')


# Supprime les fichiers existants dans le dossier cache
def vider_cache():
    if existe():
        for fichier in os.listdir(chemin):
            chemin_fichier = os.path.join(chemin, fichier)
            try:
                os.remove(chemin_fichier)
            except Exception as e:
                print('Impossible de supprimer le fichier %s. Motif : %s' % (chemin_fichier, e))


# Supprime le dossier cache
def supprimer_cache():
    if existe():
        if len(os.listdir(chemin)) != 0:
            vider_cache()
        try:
            os.rmdir(chemin)
        except Exception as e:
            print('Impossible de supprimer le dossier cache. Motif : %s' % e)
