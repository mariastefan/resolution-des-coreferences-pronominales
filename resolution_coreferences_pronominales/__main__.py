import extraction_mot
import antecedents_pronoms

if __name__ == '__main__':
    tab = extraction_mot.creation_tab_relations('aboyé', 'all')
    print(tab.info())
    print(tab.head())
    print(antecedents_pronoms.antecedents_et_verbe_des_pronoms("Le chien est tombé dans le puits. Il a aboyé."))
