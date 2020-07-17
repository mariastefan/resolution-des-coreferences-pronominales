import sys

sys.path.append(".")

import time

start = time.time()

import re
import json
from resolution_coreferences_pronominales.text_processing.tokenizer import tokenizer
from resolution_coreferences_pronominales.coreferences.mot import creation_tabs_noeuds_relations_mot

json_path = 'compound_words.json'

with open(json_path) as json_file:
    compound_words = json.load(json_file)

text = '20 vingt Le joli chat malade mange sa pâtée. Il est trop mignon celui-là. Intelligences artificielles.'
tokens = tokenizer(text)
pos = {}
ind = 0
for token in tokens:
    # Tagging punctuation tokens
    if token in ['.', ',', '!', '?', ';', '_', '&']:
        pos[ind] = 'Punct'
        ind += 1

    # If the token is a compound word we retrieve the pos tags from compound_words.json
    elif token in compound_words.keys():
        pos[ind] = compound_words[token]['POS']
        ind += 1

    # If the token is neither a punctuation nor a compound word then we get the pos tags from http://www.jeuxdemots.org/
    # throughout the function creation_tabs_noeuds_relations_mot
    else:
        tab_eids, _ = creation_tabs_noeuds_relations_mot(token.lower(), '4')
        token_pos = []
        for eid in tab_eids.keys():
            if tab_eids[eid][1] == '4':  # The relation '4' is the same as 'r_pos' on http://www.jeuxdemots.org/
                find_pos = re.findall(r"[a-zA-Z]+:*[a-zA-Z]*", tab_eids[eid][0])
                for one_pos in find_pos:
                    if ':' in one_pos:
                        token_pos.append(one_pos)
        if len(token_pos) == 0:
            sys.exit('no POS information on jdm for the token : ', token)
        elif len(token_pos) == 1:
            pos[ind] = token_pos[0]
            ind += 1
        elif len(token_pos) > 1:
            pos[ind] = token_pos
            ind += 1

for key, value in pos.items():
    print(key, ':', value)

pos_list = []
with open('list_pos', 'r') as file_list_pos:
    for line in file_list_pos.readlines():
        for i in line.split():
            if i not in pos_list:
                pos_list.append(i)
split_pos_list = []
for item in pos_list:
    for split_item in item.split(':'):
        if split_item and split_item not in split_pos_list:
            split_pos_list.append(split_item)
# print(split_pos_list)

cleaned_pos = {}
# for key, values in pos.items():
#     cleaned_pos[key] = key
#     for infos_pos in values:
#         print(':'.join(infos_pos))
#         exists = True
#         for pos_item in infos_pos:
#             for split in pos_item.split(':'):
#                 if split and split not in split_pos_list:
#                     exists = False



print(f'{time.time() - start}')
