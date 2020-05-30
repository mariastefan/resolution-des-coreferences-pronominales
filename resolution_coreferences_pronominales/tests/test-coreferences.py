import sys

sys.path.append(".")
from resolution_coreferences_pronominales import traitements_phrase

if __name__ == '__main__':
    # phrase = "Le chien est tombé dans le puits. Il va ainsi retenir la leçon."
    # phrase = "Le chien a été blessé par le puits. Il s'est cassé le museau. " \
    # phrase = "Le chien est tombé dans le puits. Il a aboyé toute la nuit."
    # phrase = "Le chat est tombé dans le puits. Il est profond. Il s'est blessé la pate."
    # phrase = "Le chien est tombé dans le puits. Il est profond."
    # phrase = "Jean est entré. Il s'est assis toute de suite."
    phrase = "Hugo s'est acheté une bicyclette. Ce moyen de transport est très écologique."


    # Phrases qui marchent certainement par hasard :
    # phrase = "Jean est entré. Il s'est assis toute de suite. Marie lui a demandé s'il pouvait
    # venir diner le lendemain."
    # phrase = "Adrien voudrait que Marie lui serve plus de gateau. Il est culotté celui-là."


    # Marchent pas :
    # phrase = "L'humain a mis un coup de poing au chien. Il lui a cassé le museau."
    # phrase = "L'humain a mis des coups de poing au chien. Il lui en a mis 3 fois."
    # phrase = "Quelqu'un qui ne le connaissait pas a demandé à Jean de lui rendre un service."
    # phrase = "Il sera comblé avant qu'il ne se blesse encore. "
    # phrase = "Jean est entré. Il s'est assis toute de suite. Marie lui a demandé si elle pouvait venir
    # diner le lendemain."
    # Ici habille n'est pas reconnu comme verbe mais comme nom, et l' comme det au lieu de pronom
    # phrase = "Jean voudrait que Marie l'habille."
    # Ici s' est bien reconnu comme un pronom mais habille est encore reconnu
    # phrase = "Jean voudrait que Marie s'habille."
    # phrase = "Adrien voudrait que Marie lui serve plus de gateau. Elle est gentille."
    # phrase = "Adrien voudrait plus de gateau. Il est culotté celui-là."





    print(phrase)

    # print(traitements_phrase.informations_pronoms(phrase))
    print(traitements_phrase.coreferences_phrase(phrase, True))
    # print(traitements_phrase.affichier_antecedents_dans_phrase(phrase, True))
