import spacy
import stanza
from flair.data import Sentence
from flair.models import SequenceTagger


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
