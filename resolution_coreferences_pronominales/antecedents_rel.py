import spacy

nlp = spacy.load('fr')


def antecedents_et_verbe_des_pronoms(phrase):
    doc = nlp(phrase)
    noms = []
    pronoms = []
    antecedents = []
    noms_ant = []
    relations_pronom = []
    i = 0
    for jeton in doc:
        i += 1
        if jeton.pos_ == 'PRON':
            j = 0
            for jetonAux in doc:
                j += 1
                if jetonAux.pos_ == 'NOUN' or jetonAux.pos_ == 'PROPN':
                    noms_ant.extend([jetonAux])
                    if 'nsubj' in jetonAux.dep_:
                        noms.append(['->', jetonAux, jeton.head])
                    if jetonAux.dep_ == 'obj':
                        noms.append(['<-', jetonAux, jeton.head])
                    if jetonAux.dep_ == 'amod':
                        noms.append([jetonAux, jetonAux.head])
                if i == j:
                    antecedents.extend([jeton, noms_ant])
                    noms_ant = []
                    if jeton.dep_ == 'nsubj':
                        relations_pronom.extend([jeton, ['->', jeton.head]])
                        pronoms.extend([jeton, [jeton.head], noms])  # relations sortantantes du pronom
                    if jeton.dep_ == 'iobj':
                        relations_pronom.extend([jeton, ['<-', jeton.head]])
                        pronoms.extend([[jeton.head], jeton, noms])  # relations entrantes vesrs le pronom
                    break
    return [antecedents,relationsPronom]
