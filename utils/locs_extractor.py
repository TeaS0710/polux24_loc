import spacy
import stanza

from flair.data import Sentence
from flair.models import SequenceTagger



SPACY_MODEL = spacy.load("trf_Precision")
STANZA_MODEL = stanza.Pipeline("fr", processors="tokenize,ner")
FLAIR_TAGGER = SequenceTagger.load("ner")

def flair(text):
    sentance = Sentence(text)
    FLAIR_TAGGER.predict(sentance)
    return sentance.get_spans("ner")

def colander_flair(ent):
    return entity.get_label("ner").value == "LOC"

def __ner_spacy(text):
    for ent in SPACY_MODEL(text).ents:
        if ent.label_ == "LOC":
            yield {
                "location": ent.text,
                "start": ent.start_char,
                "end": ent.end_char
            }


def __ner_stanza(text):
    for ent in __ner_stanza.model(text).ents:
        if ent.type == "LOC":
            yield {
                "location": ent.text,
                "start": ent.start_char,
                "end": ent.end_char
            }
    


def __ner_flair(text):
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


def get_locs(text):
    return {motor: extractor(text) for motor, extractor in get_locs.extractors.items()}
    
get_locs.extractors = {
    "flair": __ner_flair,
    "spacy": __ner_spacy,
    "stanza": __ner_stanza
}


"""

"""

def get_locs(text):
    return {motor: extractor(text) for motor, extractor in get_locs.extractors.items()}
    
get_locs.extractors = {
    "flair": __ner_flair,
    "spacy": __ner_spacy,
    "stanza": __ner_stanza
}
