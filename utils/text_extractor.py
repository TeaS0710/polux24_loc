from trafilatura import extract
from PyPDF2 import PdfReader
from os.path import splitext

def __html_text_extractor(path):
  pass


def __pdf_text_extractor(path):
  pass


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
