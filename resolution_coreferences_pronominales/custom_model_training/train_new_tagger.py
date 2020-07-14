import random
from pathlib import Path
import spacy
import sys
import os
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte

output_dir = os.path.abspath(os.path.dirname(__file__)) + '/customPOS/'
base_model = 'fr_core_news_sm'

# meta.json of the new model
lang = 'fr'
name = 'custom_sm'
description = 'Custom model based on fr_core_news_sm : French multi-task CNN trained on the ' \
                                  'French Sequoia (Universal Dependencies) and ' \
                                  'WikiNER corpus. Assigns context-specific token vectors, POS tags, dependency ' \
                                  'parse and named entities. Supports identification of PER, LOC, ORG and MISC ' \
                                  'entities.'
version = '0.0.0'


TRAIN_DATA = [
    ('I love eating', {'tags': ['PRON', 'VERB', 'VERB']}),
    ('Adrien voudrait plus de gateau. Il est culotté celui-là.',
     {'tags': ['PROPN', 'VERB', 'ADV', 'ADP', 'NOUN', 'PUNCT', 'PRON', 'VERB', 'ADJ', 'PRON','PUNCT','PRON', 'PUNCT']})
]


def train_tagger(model='fr_core_news_sm', output=None, n_iter=0):

    # Loading the model with custom tokenizer
    nlp = analyses_texte.nlp_loader()

    # Training the custom model tagger starting with the existing 'fr_core_news_sm' tagger
    nlp.vocab.vectors.name = 'spacy_pretrained_vectors'
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update([text], [annotations], sgd=optimizer, losses=losses)
        print(losses)

    # Temporary ! Testing the trained model with phrases from a file
    # ------------------------------------------------------------------------------------------ #
    test_file = open(os.path.dirname(os.path.dirname(__file__)) + "/data/phrases_test", "r")
    test_text = []
    for line, phrase in enumerate(test_file):
        if line % 2 == 0:
            test_text.append(phrase)
    docs = list(nlp.pipe(test_text))  # same as, but faster than : docs = [nlp(text) for text in textes]
    for doc in docs:
        print(doc.text)
        print([[token.text, token.pos_] for token in doc])
    # ------------------------------------------------------------------------------------------ #

    # save model to output directory
    if output is not None:
        output = Path(output)
        if not output.exists():
            output.mkdir()
        nlp.meta['lang'] = lang
        nlp.meta['name'] = name
        nlp.meta['description'] = description
        nlp.meta['version'] = version
        nlp.to_disk(output)
        print("Saved model to", output)

        # test the save model
        # Temporary ! Testing the trained model with phrases from a file
        # ------------------------------------------------------------------------------------------ #
        print("Loading from", output)
        nlp2 = spacy.load(output)
        docs = list(nlp2.pipe(test_text))
        for doc in docs:
            print(doc.text)
            print([[token.text, token.pos_] for token in doc])
        # ------------------------------------------------------------------------------------------ #


if __name__ == '__main__':
    train_tagger(base_model, output_dir)
