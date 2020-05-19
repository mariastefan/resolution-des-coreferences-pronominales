### Résolution des coréférences pronominales

#### Installation
Se placer dans le dossier `resolution-coreferences-pronominales-git` et lancer la commande suivante :\
`sh ./install.sh`
#### Exécution
Pour exécuter une démonstration sur une phrase il suffit de se placer dans le dossier `resolution-coreferences-pronominales-git` et lancer la commande suivante :\
`python3 ./resolution_coreferences_pronominales/__main__.py`
#### Désinstallation
Le fichier `uninstall.sh` sera créé après l'exécution de `install.sh`.\
`uninstall.sh` déinstallera les packages python qui n'étaient pas présents sur l'ordinateur avant l'exécution de `install.sh`.<br/> 
**Pour désinstaller :**\
Se placer dans le dossier `resolution-coreferences-pronominales-git` et lancer la commande suivante :\
`sh ./uninstall.sh`

#### Détails sur les fichiers principaux
Il y a 2 fichiers principaux qui contiennent les fonctions suivantes : 
- **extraction_mot.py**
    - `mot_sans_espaces(mot: str)`\
            ***Rend*** *le mot sans espaces*\
            *Il n'y a pas de raison d'utiliser cette fonction seule*
    - `conversion_mot(rq_word: str)`\
            ***Rend*** *rq_word sous la forme acceptée dans le lien de REZO-DUMP*\
            *Il n'y a pas de raison d'utiliser cette fonction seule*
    - `extraction_html(rq_word: str, type_relation: str)`\
            ***Rend*** *le code html correspondant depuis REZO-DUMP*\
            *Il n'y a pas de raison d'utiliser cette fonction seule*
    - `relations_mot(mot: str, type_relation: str, cache: bool)`\
            *Prend le mot, le type de la relation (pour toutes les relations alors type_relation = 'all') et cache (True ou False).*\
            ***Rend*** *une liste de listes des relations du mot, récupérées sur jeuxdemots.org, chaque* *sous-liste contenant dans*
            *l'ordre :*
         - *le nom de l'autre noeud (mot avec lequel 'mot' est en relation)*
         - *le numero du type de la relation*
         - *poids de la relation*
         - *sortante/entrante*
    - `relations_entre_mots(mots: list, cache: bool)`\
            *mots : liste des mots qui nous intéressent, ex : ["eau", "rivière", "profond"]*\
            *cache : True si on veut utiliser le cache, False sinon*\
            ***Rend*** *une liste avec toutes les relations entre les mots de la liste*
    - `vider_cache()`\
            *Vide le dossier cache*
    - `supprimer_cache()`\
            *Supprime le dossier cache*
- **traitements_phrase.py**
    - `informations_pronoms(phrase: str or spacy.tokens.doc.Doc)`\
            *Prend une phrase (de type str ou spacy.tokens.doc.Doc) et retourne des informations sur ses pronoms*\
            *Tous les mots sont lemmatisés*\
            *Quelques informations sur ce qu'on peut voir dans **infos[2]***\
            ***obj/obl*** *: à quoi fait référence le verbe (ex : "Le chien s'est cassé le museau", "museau" : obj de "cassé")*\
            ***ROOT*** *: le verbe (racine)*\
            ***xcomp*** *: complément qui donne du sens au verbe (ex : "Le chien va(ROOT) retenir(xcomp) la leçon")*\
            ***sens*** *: relation sortante/entrante (ex : "Le chien est tombé dans le puits. Il est(sortante) profond.")*\
            ***Rend*** *infos, une liste de taille 3 composé de :*
         - *infos[0] = le pronom (str)*
         - *infos[1] = [antécédents possibles] (list)*
         - *infos[2] = {d'autres infos sur le pronom, comme le verbe, le COD...} (dictionary). infos[2] peut contenir des dictionnaires, par exemple dans le cas où on a un 'xcomp' : lorsqu'on arrive sur 'xcomp' on crée un nouveau dictionnaire dans lequel on met des informations sur 'xcomp'*<br/>
        *Exemple de ce que peut rendre la fonction:*\
        `phrase = "Le chien a mordu l'humain. Il lui a cassé le museau. Il va retenir la leçon."`\
        `traitements_phrase.informations_pronoms(phrase)`\
        *Rend :* `[`<br/> 
        `['Il', ['chien', 'humain'], {'ROOT': 'casser', 'sens': 'sortante'}],`<br/> 
        `['lui', ['chien', 'humain'], {'ROOT': 'casser', 'sens': 'entrante', 'obj': 'museau'}],`<br/>
        `['Il', ['chien', 'humain', 'museau'], {'ROOT': 'aller', 'sens': 'sortante', 'xcomp': ['retenir', {'obj': 'leçon'}]}]`<br/>
        `]`
    - `coreferences_phrase(phrase: str or spacy.tokens.doc.Doc, cache: bool)`\
           **Cette fonction est le but final du projet**\
           *Prend une phrase (de type str ou spacy.tokens.doc.Doc) et retourne à quoi correspond chaque pronom*\
           ***Rend*** *une liste de listes, contenant autant de sous-listes qu'il y a de pronoms dans la phrase. Dans chaque sous-liste on retrouve un pronom et le mot auquel il fait référence.*
    - `affichier_antecedents_dans_phrase(phrase: str, cache: bool)`\
            *Utilise la fonction `coreferences_phrase()` pour :*\
           ***Rend*** *un str contenant la phrase avec les références des pronoms juste à coté des pronoms.*\
           *Ex : "Le chien est tombé dans le puits. Il(chien) s'est cassé le museau."*

