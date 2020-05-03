import spacy

nlp = spacy.load('fr')


def antecedents_et_verbe_des_pronoms(phrase):
    phrase = nlp(phrase)
    noms = []
    pronoms = []
    i = 0
    for jeton in phrase:
        if jeton.pos_ == 'PRON':
            i += 1
    j = 0
    for jeton in phrase:
        if jeton.pos_ == 'NOUN' or jeton.pos_ == 'PROPN':
            if 'nsubj' in jeton.dep_:
                noms.append(['->', jeton, jeton.head])
            if jeton.dep_ == 'obj':
                noms.append(['<-', jeton, jeton.head])
            if jeton.dep_ == 'amod':
                noms.append([jeton, jeton.head])
        if jeton.pos_ == 'PRON':
            j += 1
            if jeton.dep_ == 'nsubj':
                pronoms.extend([jeton, [jeton.head], noms])  # relations sortantes du pronom
            if jeton.dep_ == 'iobj':
                pronoms.extend([[jeton.head], jeton, noms])  # relations entrantes vers le pronom
            if i == j:
                break
    return pronoms
