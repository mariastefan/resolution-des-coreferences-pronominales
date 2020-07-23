import os
import fr_core_news_sm
from spacy.matcher import Matcher

custom_exceptions_list = ['intelligence artificielle', 'pommes de terre']
nlp = fr_core_news_sm.load()
matcher = Matcher(nlp.vocab)
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + '/models/'


def hyphen_tokens_merged():
    matcher.add('HYPHENS', None, [{'IS_ALPHA': True}, {'TEXT': '-'}, {'IS_ALPHA': True}])


def custom_tokenizer_exceptions_list(custom_list):
    for compound_word in custom_list:
        pattern = []
        for word in compound_word.split(" "):
            pattern.append({'TEXT': word})
        matcher.add(compound_word, None, pattern)


def custom_tokenizer_merger(doc):
    # this methods add matches to the matches
    hyphen_tokens_merged()
    custom_tokenizer_exceptions_list(custom_exceptions_list)

    # this will be called on the Doc object in the pipeline
    matched_spans = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_spans.append(span)
    for span in matched_spans:  # merge into one token after collecting all matches
        span.merge()
    return doc


nlp.add_pipe(custom_tokenizer_merger, first=True)  # add it right after the tokenizer
# nlp.factories['custom_tokenizer_merger'] = custom_tokenizer_merger
nlp.to_disk(model_path + 'costom_model_v1')
