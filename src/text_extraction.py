import json
import os
import sys
from logging import DEBUG

from utils import make_output, write_file, write_table, get_text
import env


def clean_source(source_path, logger):
  pass


def extract_corpus(source_path, table_path, files_path, logger):
  logger.info("")
  
  logger.debug("")
  source = clean_source(source_path, logger)
  hashes_table = {}
  
  for doc_hash, path in source.items():
    text = get_text(path, logger)
    text_hash = write_file(text, output_dir_path, logger)

    logger.debug("")
    hashes_table[doc_hash] = text_hash

  logger.debug("")
  write_table(hashes_table, output_dir_path)

  logger.info("")
  return 0


def main():
  uuid, output_dir_path, logger = make_output(PATH.OUTPUT)
  return extract_corpus(PATH.SOURCE, output_dir_path, logger)


if __name__ == "__main__":
  exit_code = main()
  sys.exit(exit_code)
