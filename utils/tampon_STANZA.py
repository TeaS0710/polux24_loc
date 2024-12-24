import stanza

stanza.download('fr')
nlp = stanza.Pipeline('fr', processors='tokenize,ner')

def read_text(path):
    with open(path_txt, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_locations_to_json(text, author):
    doc = nlp(text)
    locations = {
        f"localisation {i}": {
            "Entité": ent.text,
            "Label": ent.type
        }
        for i, ent in enumerate(doc.ents) if ent.type == "LOC"
    }

    output_file = f"{author}_stanza_locations.json"
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
