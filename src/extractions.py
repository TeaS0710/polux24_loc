from utils import FileManager, get_text, get_locs, create_logger


def extract_texts(output, source, logger):
  logger.info("Function `extract_texts` called. Start process.")
  
  for file_hash, file_metadata in source:
    with source.open(file_hash) as file:
      text = get_text(file.read(), output.logger, ext=file_metadata["ext"])
      
    output.write(text, metadata={"source": file_hash})

  logger.info("Fuction `extract_texts` done.")
  
  return 0


def main():
  logger = create_logger("text", "../cache/test.log", verbose=True, base_level=logging.DEBUG)
  with FileManager("../output/test1", "w+", output_scheme, logger) as output:
    with FileManager("../data/source", "r", source_scheme, logger) as source:
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
