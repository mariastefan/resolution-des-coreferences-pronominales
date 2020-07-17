import time

start = time.time()
import re
import json

json_path = 'compound_words.json'


def lemmatizer(text: str):
    # Opening the json file containing the list of the compound words
    with open(json_path) as json_file:
        compound_words = json.load(json_file)




if __name__ == '__main__':
    text = 'Le joli chat malade mange sa pâtée. Il est trop mignon celui-là. Les intelligences artificielles ' \
           'sont intelligentes. Le professeur veut que je rédige un compte rendu. Il veut que je me dépeche. ' \
           'Aujourd\'hui Volodia est tombé car Julien a crié. Il est méchant celui-ci. ' \
           'L\'intelligence artificielle est passionnante.'
    # text = 'Le frégate se prend un missile rapide et sombre.'
    print(lemmatizer(text))