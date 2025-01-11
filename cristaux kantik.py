import json
import os
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize

# Assurez-vous d'avoir téléchargé les ressources nécessaires de nltk
nltk.download('punkt')

def process_input_file(input_file_path):
    """
    Traite le fichier d'entrée JSON et génère les dictionnaires nécessaires
    pour volumes.json, tokens_lexicon.json et locs_lexicon.json.
    """
    # Dictionnaires pour les fichiers de sortie
    volumes = defaultdict(lambda: defaultdict(dict))
    tokens_lexicon = defaultdict(lambda: defaultdict(dict))
    locs_lexicon = defaultdict(lambda: defaultdict(dict))

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            if not line.strip():
                continue  # Ignorer les lignes vides
            try:
                doc = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON: {e}")
                continue

            doc_id = doc.get("id", "")
            author = doc.get("author", "unknown_author")
            doc_type = doc.get("type", "unknown_type")
            text = doc.get("text", "")
            size = doc.get("size", 0)
            locs = doc.get("locs", {})

            # Calculs pour volumes.json
            number_of_char = len(text)
            tokens = word_tokenize(text)
            number_of_token = len(tokens)
            weight_in_bytes = size

            volumes[author][doc_type][doc_id] = [
                number_of_char,
                number_of_token,
                weight_in_bytes
            ]

            # Calculs pour tokens_lexicon.json
            token_counts = Counter(tokens)
            tokens_lexicon[author][doc_type][doc_id] = dict(token_counts)

            # Calculs pour locs_lexicon.json
            locs_counts = defaultdict(int)
            for model, loc_list in locs.items():
                model_counts = Counter()
                for loc_range in loc_list:
                    start, end = loc_range
                    # S'assurer que les indices sont valides
                    if start < 0 or end > len(text) or start >= end:
                        continue
                    loc_text = text[start:end]
                    model_counts[loc_text] += 1
                locs_lexicon[author][doc_type][doc_id] = dict(model_counts)

    return volumes, tokens_lexicon, locs_lexicon

def write_json(output_data, output_file_path):
    """
    Écrit les données dans un fichier JSON avec une indentation pour la lisibilité.
    """
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, indent=4, ensure_ascii=False)

def main(input_file_path, output_directory):
    """
    Fonction principale qui traite le fichier d'entrée et génère les fichiers de sortie.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    volumes, tokens_lexicon, locs_lexicon = process_input_file(input_file_path)

    # Définir les chemins des fichiers de sortie
    volumes_path = os.path.join(output_directory, "volumes.json")
    tokens_lexicon_path = os.path.join(output_directory, "tokens_lexicon.json")
    locs_lexicon_path = os.path.join(output_directory, "locs_lexicon.json")

    # Écrire les fichiers de sortie
    write_json(volumes, volumes_path)
    write_json(tokens_lexicon, tokens_lexicon_path)
    write_json(locs_lexicon, locs_lexicon_path)

    print(f"Fichiers de sortie générés dans le répertoire: {output_directory}")

if __name__ == "__main__":
    # Exemple d'utilisation
    input_file = "input.json"  # Remplacez par le chemin de votre fichier d'entrée
    output_dir = "output_files"  # Remplacez par le répertoire de sortie souhaité
    main(input_file, output_dir)
