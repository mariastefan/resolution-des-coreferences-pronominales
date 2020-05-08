import extraction_mot
import antecedents_rel

if __name__ == '__main__':
    print(antecedents_rel.antecedents_et_verbe_des_pronoms("Le chien est tombé dans le puits. Il est profond"))
    for e in extraction_mot.relations_entre_mots(["chien", "puits", "profond"], True):
        print(e)
    # Il faut maintenant faire le lien entre ces fonctions
