from PyPDF2 import PdfReader
from trafilatura import extract

from utils import safecall


@safecall
def get_text(path, ext):
    if ext == "HTML":
        with open(path, "r", encoding="utf-8") as file:
            text = extract(file.read())

    elif ext == "PDF":
        text_fragments = [page.extract_text().strip() for page in PdfReader(path).pages]
        text = "\n".join(text_fragments).strip()

    elif ext == "TXT":
        with open(path, "r", encoding="utf-8") as file:
            text = file.read()
            
    else:
        raise NotImplementedError(f"Unsupported file extension: '{ext}'.")
    
    return text if text else None
