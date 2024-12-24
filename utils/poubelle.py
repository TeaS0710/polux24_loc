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


