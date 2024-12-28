import json
import os
import sys
from logging import DEBUG

from utils import make_output, get_text, write_table
import env


def write_txt(text, output_dir_path, logger):
  pass


def clean_source(source_path, logger):
  pass


def extract_corpus(source_path, output_dir_path, logger):
  logger.info("")

  logger.debug("")
  source = clean_source(source_path, logger)
  hashes_table = {}
  
  for doc_hash, path in source.items():
    text = get_text(path, logger)
    text_hash = write_txt(text, output_dir_path, logger)

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
