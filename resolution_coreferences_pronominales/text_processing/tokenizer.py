import re
import json

json_path = 'compound_words.json'


def tokenizer(text: str):
    """
    Compound words can be found in compound_words.json. The tokenizer merges those words before returning the result.
    :param text (str)
    :return: tokenized text (list)
    """

    # split_text is a list containing the text split by alphanumeric characters and hyphens, or punctuation
    split_text = re.findall(r"[\w\-]+|['.,!?;_&]", text)

    # Opening the json file containing the list with the compound words that the tokenizer must merge
    with open(json_path) as json_file:
        compound_words = json.load(json_file)

    # matches is a list containing the size and indices of the compound words found in the text
    matches = []

    # Searching for the compound words in the text and adding the size, start and end indices of the found compound
    # words to the matches
    for ind_t, token in enumerate(split_text):
        match = {'size': 0}
        for key in compound_words.keys():
            if token.lower() == key.split()[0].lower():
                if match['size'] < len(key.split()):
                    for ind_k in range(len(key.split())):
                        if split_text[ind_t + ind_k].lower() != key.split()[ind_k].lower():
                            break
                    match['size'] = len(key.split())
                    match['start'] = ind_t
                    match['end'] = ind_t + len(key.split())
        if match['size'] != 0:
            matches.append(match)

    # tokens is the list containg the return value
    tokens = []

    # Creating the final tokens list starting with the split_text and merging the compound words found in the json
    # We are also merging quote tokens with the preceding token
    ind = 0
    while ind < len(split_text):
        found = False
        for match in matches:
            if ind == match['start']:
                tokens.append(' '.join(split_text[match['start']:match['end']]))
                ind += match['size']
                found = True
        if not found:
            # Merging quotes with the preceding token
            if (ind + 1) < len(split_text) and split_text[ind + 1] == '\'':
                tokens.append(split_text[ind] + split_text[ind + 1])
                ind += 2
            else:
                tokens.append(split_text[ind])
                ind += 1

    return tokens  # list


if __name__ == '__main__':
    text = 'Le joli chat malade mange sa pâtée. Il est trop mignon celui-là. Les intelligences artificielles ' \
           'sont intelligentes. Le professeur veut que je rédige un compte rendu. Il veut que je me dépeche. ' \
           'Aujourd\'hui Volodia est tombé car Julien a crié. Il est méchant celui-ci. ' \
           'L\'intelligence artificielle est passionnante.'
    # text = 'Le frégate se prend un missile rapide et sombre.'
    print(tokenizer(text))
