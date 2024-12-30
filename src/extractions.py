from utils import FileManager, html_text_extractor, pdf_text_extractor, get_locs, create_logger


def extract_texts(output, source, logger):
  logger.info("Function `extract_texts` called. Start process.")
  
  for file_hash, file_metadata in source:
    ext = file_metadata["ext"]

    if ext == ".html":
      with source.open(file_hash) as file:
        text = html_text_extractor(file)

    elif ext == ".pdf":
      with source.open(file_hash, binary=True) as file:*
        text = pdf_text_extractor(file)

    output.write(text, metadata={"document": file_hash})

  logger.info("Fuction `extract_texts` done.")
  
  return 0


def main():
  logger = create_logger("text", "../cache/test.log", verbose=True, base_level=logging.DEBUG)

  scheme_src = {
    "url": lambda url: isinstance(url, str),
    "ext": lambda ext: ext in {".pdf", ".html"},
    "source": lambda source: isinstance(source, str)
  }

  scheme_out = {
    "document": lambda document: isinstance(document, str)
  }
  
  source = FileManager("../data/source", "r", scheme_src, logger)
  
  with FileManager("../output/test1", "w+", scheme_out, logger) as output:
    extract_texts(output, source, logger)
    
  return 0


"""
def extract_locs(output, texts):
  output.logger.info("Function `extract_locs` called. Start process.")

  for file in source.files():
    locs = get_locs(file.content, output.logger)
    output.write_json(locs, table=(file.hash))

  output.write_table()
  output.logger.info("Fuction `extract_texts` done.")

  return 0
  """
