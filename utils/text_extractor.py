from trafilatura import extract
from PyPDF2 import PdfReader
from os.path import splitext
import glob
import trafilatura

def html_text_extractor(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        text = trafilatura.extract(html_content)
        if text is None:
            print(f"Aucun texte pertinent n'a été extrait du fichier {file_path}.")
            return ""
        return text
        
def pdf_text_extractor(path):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        if text is None:
            print(f"Aucun texte pertinent n'a été extrait du fichier {path}.")
            return ""
        return text

class TextExtractor:
  extractors = {
    ".html": __html_text_extractor,
    ".pdf": __pdf_text_extractor
  }

  @staticmethod
  def get_text(path):
    ext = splitext(path)[-1].lower()
    extractor = TextExtractor.extractors.get(ext, None)

    if extractor is None:
      raise NotImplementedError(f"TextExtractor doesn't support '{ext}' files.")

    return extractor(path)
