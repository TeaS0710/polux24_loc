import stanza
import json
import glob

# Chemins des fichiers texte
paths = glob.glob(r"..\ressources_TD6\Texte\*\*\*.txt")

# Initialisation du pipeline Stanza
stanza.download('fr')  # Télécharge les modèles pour le français si nécessaire
nlp = stanza.Pipeline('fr', processors='tokenize,ner')

def read_text(path_txt):
    """Lit le contenu d'un fichier texte."""
    with open(path_txt, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_locations_to_json(text, author):
    """Extrait les entités de type localisation et les enregistre dans un fichier JSON."""
    doc = nlp(text)
    
    # Filtrer uniquement les entités de type LOCALISATION (LOC)
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
    return output_file

def count_locations(json_file):
    """Compte les occurrences des localisations extraites."""
    with open(json_file, mode='r', encoding='utf-8') as f:
        locations = json.load(f)
    return len(locations)

def main():
    for path in paths:
        # Récupérer l'auteur depuis le chemin
        author = path.split("\\")[-3]
        text = read_text(path)
        print(f"Traitement : {path}")
        output_file = extract_locations_to_json(text, author)
        location_count = count_locations(output_file)
        print(f"Nombre de localisations extraites dans {output_file}: {location_count}")

if __name__ == "__main__":
    main()
