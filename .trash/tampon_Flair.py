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
                txt= ent.text
            )
    return locentities

def main():
    locations = extract_locations(key, txt)
    print(locations)
    
main()
