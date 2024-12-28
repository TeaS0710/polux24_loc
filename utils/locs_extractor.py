import spacy
import stanza
from flair.data import Sentence
from flair.models import SequenceTagger

import stanza
import flair
from flair.data import Sentence
from flair.models import SequenceTagger

tagger = SequenceTagger.load('ner')

def extract_locations_to_json(key, txt):
    sentence = Sentence(text)
    nlp = tagger.predict(sentence)
    doc = nlp(txt)

    locentities = []

    for ent in doc.ents:
        if ent.type == "LOC":
            yield LocEntity(
                document= key,
                start= ent.start_char,
                end= ent.end_char,
                motor=f"{model_lang}",
                text= ent.text
            )
    return locentities

def main():
    locations = extract_locations(key, txt)
    print(locations)
    
main()

def extract_locations(key, txt):

    stanza.download('fr')
    nlp = stanza.Pipeline('fr', processors='tokenize,ner')

    doc = nlp(txt)
    locentities = []

    for ent in doc.ents:
        if ent.type == "LOC":
            yield LocEntity(
                document= key,
                start= ent.start_char,
                end= ent.end_char,
                motor="stanza",
                text= ent.text
            )
    return locentities

def main():
    locations = extract_locations(key, txt)
    print(locations)
    
    main()

import spacy
from spacy import displacy
import json

#python -m spacy download fr_dep_news_trf
#python -m spacy download fr_core_news_lg

Modele_version = "trf"
if Modele_version == "lg_Efficiency":
    Modele = "fr_core_news_lg"
elif Modele_version == "trf_Precision":
    Modele = "fr_dep_news_trf"

def extract_locations(txt, model_lang, key):
    nlp = spacy.load(model_lang)
    doc = nlp(txt)

    locentities = []

    for ent in doc.ents:
        if ent.type == "LOC":
            yield LocEntity(
                document= key,
                start= ent.start_char,
                end= ent.end_char,
                motor=f"{model_lang}",
                text= ent.text
            )
    return locentities

def main():
    locations = extract_locations(key, txt)
    print(locations)
    
    main()

class NerModeWrapper:
    model = None
    
    def ents(self, text):
        raise NotImplementedError

    def filter(self, ent):
        raise NotImplementedError

    def ents_to_dict(self, ent):
        raise NotImplementedError

    def ner(self, text):
        return [self.ents_to_dict(entity) for entity in self.ents(text) if self.filter(entity)]


class SpacyAndStanzaBase(NerModeWrapper):
    def ents(self, text):
        # Utilisation de self.model au lieu de 'model'
        return self.model(text).ents

    def ents_to_dict(self, ent):
        return {
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char
        }


class SpacyNerModel(SpacyAndStanzaBase):
    model = spacy.load("trf_Precision")

    def filter(self, ent):
        return ent.label_ == "LOC"


class StanzaNerModel(SpacyAndStanzaBase):
    model = stanza.Pipeline("fr", processors="tokenize,ner")

    def filter(self, ent):
        return ent.type == "LOC"


class FlairNerModel(NerModeWrapper):
    model = SequenceTagger.load("ner")
    
    def ents(self, text):
        sentence = Sentence(text)
        self.model.predict(sentence)
        return sentence.get_spans("ner")

    def filter(self, entity):
        return entity.get_label("ner").value == "LOC"

    def ents_to_dict(self, ent):
        return {
            "start": ent.start_position,
            "end": ent.end_position,
            "location": ent.text
        }


def get_locs(text):
    return {motor_name: motor.ner(text) for motor_name, motor in get_locs.extractors.items()}
    
get_locs.extractors = {
    "flair": FlairNerModel(),
    "spacy": SpacyNerModel(),
    "stanza": StanzaNerModel()
}
