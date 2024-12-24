from os.path import splitext
from PyPDF2 import PdfReader
from trafilatura import extract


def __html_text_extractor(path):
    with open(path, "r", encoding="utf-8") as file:
        text = extract(file.read())
        
    return text if text else ""

        
def __pdf_text_extractor(path):
    text = [page.extract_text().stip() for page in PdfReader(path).pages]
    final_text = "\n".join(text).strip()
    
    return final_text if final_text else ""


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
