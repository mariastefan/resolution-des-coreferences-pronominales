import sys
from functools import reduce
from resolution_coreferences_pronominales.text_processing.sort_pos_sequences import pos_sequences_out_path
sys.path.append(".")

import time

start = time.time()
import pickle
import re
import json
from resolution_coreferences_pronominales.text_processing.tokenizer import tokenizer
from resolution_coreferences_pronominales.coreferences.mot import creation_tabs_noeuds_relations_mot

pos_sequences_path = 'data/pos_sequences_sorted.pkl'
json_path = 'data/compound_words.json'


def splitkeepsep(string: str, sep: str):
    '''
    Split string keeping the separator
    :param string:
    :param sep:
    :return: split string
    '''
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem],
                  re.split("(%s)" % re.escape(sep), string), [])


def pos_candidates_jdm(text: str):
    '''
    Searches in http://www.jeuxdemots.org/rezo-dump.php for the r_pos relations for each token in text
    :param text (str)
    :return: pos_candidates (dict)
    '''
    tokens = tokenizer(text)
    pos_candidates = {}
    ind = 0
    with open(json_path) as json_file:
        compound_words = json.load(json_file)
    for token in tokens:
        # Tagging punctuation tokens
        if token in ['.', ',', '!', '?', ';', '_', '&']:
            pos_candidates[ind] = 'Punct'
            ind += 1

        # If the token is a compound word we retrieve the pos tags from compound_words.json
        elif token in compound_words.keys():
            pos_candidates[ind] = compound_words[token]['POS']
            ind += 1

        # If the token is neither a punctuation nor a compound word then we get the pos tags from http://www.jeuxdemots.org/
        # throughout the function creation_tabs_noeuds_relations_mot
        else:
            tab_eids, _ = creation_tabs_noeuds_relations_mot(token.lower(), '4')
            keys_to_delete = []
            for key, value in tab_eids.items():
                if value[1] != '4':
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del tab_eids[key]
            if len(tab_eids) == 0:
                tab_eids, _ = creation_tabs_noeuds_relations_mot(token, '4')
            token_pos = []
            for eid in tab_eids.keys():
                if tab_eids[eid][1] == '4':  # The relation '4' is the same as 'r_pos' on http://www.jeuxdemots.org/
                    find_pos = re.findall(r"[a-zA-Z0-9]+[:*[a-zA-Z0-9]*]*", tab_eids[eid][0])
                    for one_pos in find_pos:
                        if ':' in one_pos:
                            token_pos.append(one_pos)
            if len(token_pos) == 0:
                sys.exit('no POS information on jdm for the token : ' + token)
            elif len(token_pos) == 1:
                pos_candidates[ind] = token_pos[0]
                ind += 1
            elif len(token_pos) > 1:
                pos_candidates[ind] = token_pos
                ind += 1

    return pos_candidates


def load_pos_sequences(text: str):
    pos_candidates = pos_candidates_jdm(text)
    useful_sequences = []
    try:
        seq_file = open(pos_sequences_out_path, 'rb')
    except Exception as e:
        sys.exit('Impossible de créer le fichier ' + pos_sequences_out_path + '\nMotif : %s' % e)
    sequences = pickle.load(seq_file)
    for sequence in sequences:
        if len(sequence) == len(pos_candidates):
            useful_sequences.append(sequence)
    return useful_sequences


def pos(text: str):
    phrases = splitkeepsep(text, '.')
    all_pos_sequences = []
    for phrase in phrases:
        if phrase:
            phrase_pos_sequences = []
            sequences = load_pos_sequences(phrase)
            pos_candidates = pos_candidates_jdm(phrase)
            size = len(pos_candidates) if sequences and pos_candidates else 0
            if size != 0:
                for sequence in sequences:
                    found_one = []
                    found_all = True
                    for key, pos_candidate in pos_candidates.items():
                        if isinstance(pos_candidate, str):
                            if pos_candidate in sequence[key]:
                                found_one.append(True)
                                break
                        else:
                            for one_pos in pos_candidate:
                                if one_pos in sequence[key]:
                                    found_one.append(True)
                                    break
                        if len(found_one) != key + 1:
                            found_one.append(False)
                            break
                    for value in found_one:
                        if not value:
                            found_all = False
                    if found_all:
                        phrase_pos_sequences.append(sequence)
            if len(phrase_pos_sequences) > 1:
                max_len = 0
                ind = 0
                for tmp_ind, phrase_pos in enumerate(phrase_pos_sequences):
                    if len(str(phrase_pos)) > max_len:
                        max_len = len(str(phrase_pos))
                        ind = tmp_ind
                all_pos_sequences += phrase_pos_sequences[ind]
            elif len(phrase_pos_sequences) == 1:
                all_pos_sequences += phrase_pos_sequences[0]
            else:
                sys.exit('No POS sequence found for the phrase : ' + phrase)

    return all_pos_sequences

    # for ind in range(size):
    #     if pos_candidates[ind] != sequences[ind]:


if __name__ == '__main__':
    txt = 'Adrien voudrait plus de gateau. Il est culotté celui-là.'

    # seq = pos_sequences(txt)
    # for i in seq:
    #     print(i)

    pos = pos(txt)
    print(pos)

    # pos = pos_candidates_jdm(txt)
    # for i,j in pos.items():
    #     print(i,j)

    print(f'{time.time() - start}')
