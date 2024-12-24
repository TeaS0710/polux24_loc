import flair
from flair.data import Sentence
from flair.models import SequenceTagger
import json

tagger = SequenceTagger.load('ner')

def read_text(path_txt):
    with open(path_txt, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_locations_to_json(text, author):
    sentence = Sentence(text)
    tagger.predict(sentence)
    
    locations = {
        f"localisation {i}": {
            "Entité": entity.text,
            "Label": entity.get_label("ner").value
        }
        for i, entity in enumerate(sentence.get_spans('ner')) if entity.get_label("ner").value == "LOC"
    }

    output_file = f"{author}_flair_locations.json"
    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(locations, f, indent=4)
    print(f"Fichier JSON généré : {output_file}")
    return output_file, author, location

def main():
    for path in paths:
        author = path.split("\\")[-3]
        text = read_text(path)
        print(f"Traitement : {path}")
        output_file = extract_locations_to_json(text, author)
        print(f"Nombre de localisations extraites dans {output_file}: {location_count}")

main()
