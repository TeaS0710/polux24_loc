from utils import FileManager, get_text, get_locs


def extract_texts(output, source):
  output.logger.info("Function `extract_texts` called. Start process.")
  
  for file in source.files():
    text = get_text(file.content, output.logger, ext=file.ext)
    output.write_text(text, table=(file.hash))

  output.write_table()
  output.logger.info("Fuction `extract_texts` done.")
  
  return 0


def extract_locs(output, texts):
  output.logger.info("Function `extract_locs` called. Start process.")

  for file in source.files():
    locs = get_locs(file.content, output.logger)
    output.write_json(locs, table=(file.hash))

  output.write_table()
  output.logger.info("Fuction `extract_texts` done.")

  return 0
