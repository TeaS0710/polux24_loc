import os
import json

from .sha256 import hash_str


def write_file(content, dir_path, logger):
  pass


def write_table(dir_path, logger):
  pass


def split_path(path):
  pass


def make_output_dir(output_dir_path, log_dir_path):
  uuid = generate_uuid()
  
  output_dir_path = os.path.join(dir_path, uuid)
  os.makedirs(output_dir_path)

  log_path = os.path.join(log_dir_path, f"{uuid}.log")
  logger = create_logger()
  
  return uuid, output_dir_path
  
