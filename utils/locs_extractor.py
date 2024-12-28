from spacy import load as spacy_load
from stanza import Pipeline as stanza_load
from flair.data import Sentence
from flair.models.SequenceTagger import flair_load



def __ner_flair(text):
    sentence = Sentence(text)
    __ner_flair.model.predict(sentence)
    return [
        {"start": ent.start_position, "end": ent.end_position, "location": ent.text}
        for ent in sentence.get_spans("ner")
        if ent.get_label("ner").value == "LOC"
    ]

__ner_flair.model = flair_load("ner")


def __ner_spacy(text):
    return [
        {"text": ent.text, "start": ent.start_char, "end": ent.end_char}
        for ent in __ner_spacy.model(text).ents
        if ent.label_ == "LOC"
    ]

__ner_spacy.model = spacy_load("fr_dep_news_trf")


def __ner_stanza(text):
    return [
        {"text": ent.text, "start": ent.start_char, "end": ent.end_char}
        for ent in model(text).ents
        if ent.type == "LOC"
    ]

__ner_stanza.model = stanza_load("fr", processors="tokenize,ner")


def get_locs(text):
    return {motor_name: motor(text) for motor_name, motor in get_locs.extractors.items()}
    
get_locs.extractors = {
    "flair": __ner_flair,
    "spacy": __ner_spacy,
    "stanza": __ner_stanza
}
