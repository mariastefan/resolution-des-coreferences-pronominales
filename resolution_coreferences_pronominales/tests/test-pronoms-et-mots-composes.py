import sys
import os

sys.path.append(".")
from resolution_coreferences_pronominales.custom_model_training import custom_tokenizer

filename = os.path.basename(__file__)
print('Start : ' + filename)
text = 'intelligences artificielles intelligence artificielle bandes dessinées bande dessinée comptes rendus compte ' \
       'rendu faux sens faux sens hôtels de ville hôtel de ville'
nlp = custom_tokenizer.nlp_loader()
doc = nlp(text)
for token in doc:
    try:
        assert ' ' in token.text
    except AssertionError:
        sys.exit('Tokenizer error, a token which is meant to be compound is not : ' + token.text)
    if token.i % 2 == 0:
        try:
            assert token.lemma_ == doc[token.i + 1].text
        except AssertionError:
            sys.exit(filename + ' : Tokenizer error, problem with : "' + token.text + '" or/and it\'s lemma : "' +
                     doc[token.i + 1].text + '"')
print('Completed : ' + filename)
