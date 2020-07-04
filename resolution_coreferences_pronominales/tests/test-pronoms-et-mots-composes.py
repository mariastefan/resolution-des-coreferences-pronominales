import sys
import spacy
import fr_core_news_sm
sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte

phrase = u'Aujourd\'hui Volodia est tombé car Julien a crié. Il est méchant celui-là. L\'intelligence artificielle ' \
         u'est passionnante.'
nlp = analyses_texte.nlp_loader()
doc = nlp(phrase)
print([token.text for token in doc])
