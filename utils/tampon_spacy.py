import spacy
from spacy import displacy
import json
import glob
from collections import Counter

# Chemins des fichiers texte
paths = glob.glob(r"..\ressources_TD6\Texte\*\*\*.txt")

# Choix du modèle spaCy
Modele_version = "trf"  # Choisissez entre "sm" (small), "lg" (large), ou "trf" (transformer)
if Modele_version == "sm":
    Modele = "fr_core_news_sm"
elif Modele_version == "lg":
    Modele = "fr_core_news_lg"
elif Modele_version == "trf":
    Modele = "fr_dep_news_trf"

def read_text(path_txt):
    """Lit le contenu d'un fichier texte."""
    with open(path_txt, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_locations_to_json(text, model_lang, author):
    """Extrait les entités de type localisation et les enregistre dans un fichier JSON."""
    nlp = spacy.load(model_lang)
    nlp.max_length = 1000000  # Ajuster si besoin pour les très longs textes
    doc = nlp(text)
    
    # Filtrer uniquement les entités de type LOCALISATION (LOC)
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
        output_file = extract_locations_to_json(text, Modele, author)
        location_count = count_locations(output_file)
        print(f"Nombre de localisations extraites dans {output_file}: {location_count}")

main()
