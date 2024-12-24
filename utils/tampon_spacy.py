import spacy

def read_text(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_locations_to_json(text, model_lang, author):
    nlp = spacy.load(model_lang)
    nlp.max_length = 1000000 
    doc = nlp(text)

    locations = {
        f"localisation {i}": {
            "Entité": ent.text,
            "Label": ent.label_
        }
        for i, ent in enumerate(doc.ents) if ent.label_ == "LOC"
    }
  
    output_file = f"{author}_{model_lang}_locations.json"

    return locations, output_file, author, model_lang

