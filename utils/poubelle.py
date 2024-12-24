import glob
from trafilatura import extract

#fonction extraction HTML to TXT
def extract_TEXT_HTML(folder_path):

    extracted_texts = {}
    
    # Utilisation de glob pour trouver tous les fichiers HTML
    html_files = glob.glob(f"{folder_path}/**/*.html", recursive=True)
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Extraction du texte via Trafilatura
        text = extract(html_content)
        extracted_texts[file_path] = text or ""
    return extracted_texts

# folder_path = "/chemin/vers/le/dossier"
# texts = extract_TEXT_HTML(folder_path)

#Fonction d'extraction PDF TO TXT

from PyPDF2 import PdfReader

def extract_text_from_pdfs(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du PDF {file_path}: {e}")
        return text


#Fonction REN VIA SPACY

import spacy
from spacy import displacy
import json
import glob
from collections import Counter

paths = glob.glob(r"..\ressources_TD6\Texte\*\*\*.txt")
Modele_version = "trf"  # Choisissez entre "sm" (small) et "lg" (large)
if Modele_version == "sm":
    Modele = "fr_core_news_sm"
elif Modele_version == "lg":
    Modele = "fr_core_news_lg"
elif Modele_version == "trf":
    Modele = "fr_dep_news_trf"

def read_text(path_txt):
    with open(path_txt, mode='r', encoding='utf-8') as f:
        return f.read()

def extract_entities_to_json(text, model_lang, author):
    nlp = spacy.load(model_lang)
    nlp.max_length = 1000000  # Ajuster si besoin pour les très longs textes
    doc = nlp(text)
    entities = {
        f"entité {i}": {
            "Entité": ent.text,
            "Label": ent.label_
        }
        for i, ent in enumerate(doc.ents)
    }
    output_file = f"{author}_{model_lang}_spacy.json"
    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(entities, f, indent=4)
    print(f"Fichier JSON généré : {output_file}")
    return output_file

def count_entities_by_category(json_file):
    with open(json_file, mode='r', encoding='utf-8') as f:
        entities = json.load(f)
    categories = [ent["Label"] for ent in entities.values()]
    category_counts = Counter(categories)
    return category_counts

def main():
    for path in paths:
        # Récupérer l'auteur depuis le chemin
        author = path.split("\\")[-3]
        text = read_text(path)
        print(f"Traitement : {path}")
        output_file = extract_entities_to_json(text, Modele, author)
        category_counts = count_entities_by_category(output_file)
        print(f"Compte des catégories dans {output_file}:")
        for category, count in category_counts.items():
            print(f"{category}: {count}")

main()
