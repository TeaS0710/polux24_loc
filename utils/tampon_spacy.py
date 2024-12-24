import spacy
from spacy import displacy
import json

Modele_version = "trf"
if Modele_version == "sm":
    Modele = "fr_core_news_sm"
elif Modele_version == "lg":
    Modele = "fr_core_news_lg"
elif Modele_version == "trf":
    Modele = "fr_dep_news_trf"

def read_text(path_txt):
    with open(path_txt, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_locations_to_json(text, model_lang, author):
    nlp = spacy.load(model_lang)
    nlp.max_length = 1000
    doc = nlp(text)

    locations = {
        f"localisation {i}": {
            "Entité": ent.text,
            "Label": ent.label_
        }
        for i, ent in enumerate(doc.ents) if ent.label_ == "LOC"
    }

    output_file = f"{author}_{model_lang}_locations.json"
    
    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(locations, f, indent=4)
    print(f"Fichier JSON généré : {output_file}")
    return output_file, author, model_lang, locations

def main():
    for path in paths:
        author = path.split("\\")[-3]
        text = read_text(path)
        print(f"Traitement : {path}")
        output_file = extract_locations_to_json(text, Modele, author)
        print(f"Nombre de localisations extraites dans {output_file}: {location_count}")

main()
