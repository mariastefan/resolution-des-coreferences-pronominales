import sys
import os
import time

sys.path.append(".")
from resolution_coreferences_pronominales.custom_model_training import custom_tokenizer

if __name__ == '__main__':
    phrases_test = open(os.path.dirname(os.path.dirname(__file__)) + "/data/phrases_test", "r")
    start = time.time()
    textes = []
    nlp = custom_tokenizer.nlp_loader()
    for numero_ligne, phrase in enumerate(phrases_test):
        if numero_ligne % 2 == 0:
            textes.append(phrase)
    docs = list(nlp.pipe(textes))  # same as, but faster than : docs = [nlp(text) for text in textes]
    print(time.time() - start)
    print(nlp.pipe_names)
    start = time.time()
    for doc in docs:
        print('\n', doc.text, end='')
        print([[token.text, token.pos_, token.dep_] for token in doc])
    print(str(time.time() - start))
