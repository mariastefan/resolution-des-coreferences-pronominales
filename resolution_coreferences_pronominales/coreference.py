import extraction_mot
import antecedents_rel

def coreferences(phrase):
    antecedents_relations=antecedents_rel.antecedents_et_verbe_des_pronoms(phrase)
    antecedents=antecedents_relations[0]
    relationsPronom=antecedents_relations[1]
    print(antecedents,relationsPronom)
    i=0
    j=0
    while (i<len(relationsPronom) and j<len(antecedents)):
        antecedent=antecedents[j+1]
        prn=relationsPronom[i]
        if(len(antecedent)==1):
            print("le pronom",prn,"fait references à ",antecedent[0],"et je suis bien la ou il faut")
            break
    
        relations=relationsPronom[i+1]
        if(relations[0]=='->'):
            del relations[0]
            for mot in relations:
                print(mot)
                relations_mot = extraction_mot.relations_mot(str(mot),'all',1)
                if relations_mot is None:
                    print("il est bien null")
                    break
                for rid in relations_mot.values():
                    for world in antecedent:
                        if str(world) == str(rid[0]):
                            print("le pronom",prn,"fait references à",world)
                                        
        i+=2
        j+=2

phrase="Le chien est tombé dans le puit. Il a aboyer toute la nuit."
coreferences(phrase)
