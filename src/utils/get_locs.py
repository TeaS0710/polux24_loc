from spacy import load
from stanza import Pipeline
from flair.data import Sentence


FLAIR = SequenceTagger("ner")
SPACY = load("fr_dep_news_trf")
STANZA = Pipeline("fr")  

def get_locs(text):
    locs = {}

    sentence = Sentence(text)
    FLAIR.predict(sentence)
    locs["flair"] = [
        [ent.start_position, ent.end_position]
        for ent in sentence.get_spans("ner")
        if ent.get_label("ner").value == "LOC"
    ]

    locs["spacy"] = [
        [ent.start_char, ent.end_char]
        for ent in SPACY(text).ents
        if ent.label_ == "LOC"
    ]

    locs["stanza"] = [
        [ent.start_char, ent.end_char]
        for ent in STANZA(text).ents
        if ent.type == "LOC"
    ]
    
    return locs
