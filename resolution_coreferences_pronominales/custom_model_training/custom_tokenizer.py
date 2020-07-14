import fr_core_news_sm
import os
from spacy.matcher import Matcher
import json
from spacy.language import Language
from spacy.tokens import Doc

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + \
            '/custom_model_training/custom_model_params/compound_words.json'


def nlp_loader():
    """
    Temporary fonction allowing to load the nlp with the custom tokenizer.
    This will later become a fonction creating a new model and scripts will no longer be loading the model with
    this fonction but directly from the new customized model
    :return: nlp
    """
    nlp = fr_core_news_sm.load()

    class CompoundWordsMerger:
        def __init__(self, words_path):
            # self.model_size = model_size
            self.words_path = words_path

        def __call__(self, doc: Doc):
            # Adding hyphen compound words to the matcher
            matcher = Matcher(nlp.vocab)
            matcher.add('HYPHENS', None, [{'IS_ALPHA': True}, {'TEXT': '-'}, {'IS_ALPHA': True}])

            # Opening the json file containing the information about our custom compound words
            with open(self.words_path) as json_file:
                compound_words = json.load(json_file)

            # Creating a list which will contain the keys of the dictionary in words_path json file
            # These keys correspond to the custom compound words text
            custom_exceptions_list = []
            for key in compound_words.keys():
                custom_exceptions_list.append(key)

            # Adding the custom compound words from the json file to the matcher
            for word in custom_exceptions_list:
                pattern = []
                for word in word.split(' '):
                    pattern.append({'TEXT': word})
                matcher.add(word, None, pattern)

            # Adding the matches containing the compound words to the doc
            matched_spans = []
            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                matched_spans.append(span)
                if str(span) in compound_words.keys():
                    nlp.tokenizer.add_special_case(str(span),
                                                   [{'ORTH': str(span), 'POS': compound_words[str(span)]["pos"]}])
            for span in matched_spans:  # merge into one token after collecting all matches
                span.merge()

            # Adding the custom lemmas for the custom compound words
            for token in doc:
                if ' ' in token.text:
                    if token.text in compound_words.keys():
                        token.lemma_ = compound_words[token.text]["lemma"]

            return doc

    nlp.add_pipe(CompoundWordsMerger(json_path),
                 first=True)  # , first=True : add it right after the tokenizer; default : last

    # Adding the custom pipeline to the factories
    Language.factories['CompoundWordsMerger'] = lambda _: CompoundWordsMerger(json_path)
    return nlp
