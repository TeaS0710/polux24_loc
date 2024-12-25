import logging
import time

from os.path import basename, splitext
from os.path import join as os_join


def new_logger(caller_path, dir_path, level=logging.DEBUG, verbose=False):
    timestamp = int(time.time())
    stem, _ = splitext(basename(caller_path))
    log_path = os_join(dir_path, f"{stem}_{timestamp}.log")

    logger = logging.getLogger(log_path)
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.debug(f"Log file opened by '{caller_path}'.")
    
    return logger
