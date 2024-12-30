from PyPDF2 import PdfReader
from trafilatura import extract

from .misc_tools import split_path, exists


def __html_text_extractor(path):
    """
    Extracts text from an HTML file.

    Retrieves HTML file content and calls :func:`trafilatura.extract` to extract text.

    .. warning::
       This function is meant for internal use and should not be called directly by the user.
       Existence and file type checks are not performed, so errors may be raised.

    Related objects:
    - :mod:`trafilatura`
    - :func:`trafilatura.extract`

    :param path: Path of the HTML file.
    :returns: Text extracted from the HTML file.

    :type path: str
    :rtype: str
    """

    # Open `path` in read mode as `file`, and pass file content (e.g., `file.read()`) to `trafilatura.extract`
    with open(path, "r", encoding="utf-8") as file:
        text = extract(file.read())

    # Return `text` or an empty string if extraction fails
    return text if text else ""

        
def __pdf_text_extractor(path):
    """
    Extracts text from a PDF file.

    Uses :class:`PyPDF2.PdfReader` to iterate through PDF pages.
    Retrieves text from each page with the :func:`extract_text` method.

    .. warning::
       This function is meant for internal use and should not be called directly by the user.
       Existence and file type checks are not performed, so errors may be raised.

    Related objects:
    - :mod:`PyPDF2`
    - :class:`PyPDF2.PdfReader`

    :param path: Path of the PDF file.
    :returns: Text extracted from the PDF file.

    :type path: str
    :rtype: str
    """

    # List comprehension that iterates through each page of `path` and extracts their text
    text_fragments = [page.extract_text().strip() for page in PdfReader(path).pages]

    # Build final `text` by concatenating `text_fragments`
    text = "\n".join(text_fragments).strip()

    # Return `text` or an empty string if extraction fails
    return text if text else ""


def get_text(path, logger):
    """
    Extracts text from a file.

    Calls the appropriate extractor function based on the file extension.

    .. note::
       Implements error handling via the logger, so it can be safely called without crashing the program.

    Related objects:
    - :func:`__html_text_extractor`
    - :func:`__pdf_text_extractor`

    :param path: Path of the file.
    :param logger: Logger instance for handling logs.
    :returns: Text extracted from the file.

    :type path: str
    :type logger: logging.Logger
    :rtype: str

    :ivar extractors: A mapping of file extensions to their respective text extractor functions.
    :vartype extractors: Dict[str, Callable[[str], str]]
    """

    logger.debug("Function `get_text` called.")

    # Check if the file exists
    logger.debug(f"Checking if '{path}' exists.")
    if not exists(path):
        logger.error(f"Cannot run extraction on '{path}': file not found.")

    # Retrieve the appropriate extractor based on the file extension
    logger.debug(f"Trying to get an extractor for '{path}'.")
    _, ext = split_path(path)
    extractor = get_text.extractors.get(ext, None)

    # Check if the extractor exists
    logger.debug(f"Checking if an extractor was found for '{ext}' files.")
    if extractor is None:
        logger.error(f"Cannot run extraction on '{path}': no extractor found for '{ext}' files.")
        text = ""
    else:
        #execute l'extraction avec une gestion d'erreur
        try:
            logger.debug(f"Running extraction on '{path}'.")
            text = extractor(path)

        except Exception as exception:
            logger.error(f"Extraction of '{path}' failed: '{exception}'.")
            text = ""

    # Log success if text is extracted
    if text:
        logger.info(f"Text successfully extracted from '{path}' ({len(text)} character(s) extracted).")
    
    # Log warning if no text is extracted
    else:
        logger.warning(f"No text extracted from '{path}': an error may have occurred during the process, or the file is empty.")

    logger.debug("Function `get_text` completed.")
    return text

# Adds extractor table to `get_text`
    get_text.extractors = {
    ".html": __html_text_extractor,
    ".pdf": __pdf_text_extractor
}
