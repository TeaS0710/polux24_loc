import spacy
from spacy import displacy
import stanza
from flair.data import Sentence
from flair.models import SequenceTagger

# python -m spacy download fr_dep_news_trf
# python -m spacy download fr_core_news_lg

MODELE_VERSION = "trf_Precision"
if MODELE_VERSION == "lg_Efficiency":
    MODELE = "fr_core_news_lg"
elif MODELE_VERSION == "trf_Precision":
    MODELE = "fr_dep_news_trf"

def extract_locations_spacy(txt, model_lang, key):
    nlp = spacy.load(model_lang)
    doc = nlp(txt)
    for ent in doc.ents:
        if ent.label_ == "LOC":
            yield LocEntity(
                document=key,
                start=ent.start_char,
                end=ent.end_char,
                motor=model_lang,
                text=ent.text
            )

def extract_locations_stanza(key, txt):
    stanza.download('fr')
    nlp = stanza.Pipeline('fr', processors='tokenize,ner')
    doc = nlp(txt)
    for ent in doc.ents:
        if ent.type == "LOC":
            yield LocEntity(
                document=key,
                start=ent.start_char,
                end=ent.end_char,
                motor="stanza",
                text=ent.text
            )

def extract_locations_flair(key, txt):
    tagger = SequenceTagger.load('ner')
    sentence = Sentence(txt)
    tagger.predict(sentence)
    for entity in sentence.get_spans('ner'):
        if entity.get_label("ner").value == "LOC":
            yield LocEntity(
                document=key,
                start=entity.start_position,
                end=entity.end_position,
                motor="flair",
                text=entity.text
            )

class RENextractor:
    def __init__(self):
        self.extractors = {
            "spacy": extract_locations_spacy,
            "stanza": extract_locations_stanza,
            "flair": extract_locations_flair
        }

    def extract(self, method, key, txt):
        if method not in self.extractors:
            raise ValueError(f"Méthode inconnue : {method}")
        return list(self.extractors[method](key, txt))

def main():
    extractor = RENextractor()

    print("Extraction avec SpaCy:")
    print(extractor.extract("spacy", txt, MODELE))
    print("\nExtraction avec Stanza:")
    print(extractor.extract("stanza", key, txt))
    print("\nExtraction avec Flair:")
    print(extractor.extract("flair", key, txt))
main()
