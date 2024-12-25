import json
import lmdb
import sys

from hashlib import md5
from os.path import splitext, exists

from utils import Document, new_logger
from env import PATH, VARS


def compute_md5(utf8_str):
    return md5(utf8_str.encode("utf-8")).hexdigest()


def clean_table(hash_table, logger):
    logger.info("Function 'clean_table' called.")
    
    cleaned_table = {}
    initial_size = len(hash_table)
    
    for key, data in hash_table.items():        
        match data:
            case {"author": str(author), "group": str(group), "path": str(path), "url": str(url)}:
                _, ext = splitext(path)
                
                if ext not in Document.supported_exts:
                    logger.debug(f"Unsupported file extension: '{key}' skipped.")
                    continue
                
                if not exists(path):
                    logger.debug(f"File path does not exist: '{key}' skipped.")
                    continue
            
                if key != compute_md5(url):
                    logger.debug(f"Mismatch between 'hash' and 'url': '{key}' skipped.")
                    continue
                
            case _:
                logger.debug(f"Invalid data structure: '{keys}' skipped.")
                continue
        
        cleaned_table[key] = data
        logger.debug(f"Verified key added: '{key}' matches all the requirements.")
    
    cleaned_size = len(cleaned_table)
    
    if cleaned_size < initial_size:
        logger.warning(f"{initial_size - cleaned_size} document(s) removed from the original hash table.")
    
    logger.info(f"Function 'clean_table' completed successfully.")
    return cleaned_table


def add_documents(txn, hash_table, logger):
    logger.warning("Function 'add_documents' called.")
    
    added_docs = 0
    total = 0
    
    txn.drop(delete=False)
    logger.debug("Database cleared for rewriting.")
    
    for key, data in hash_table.items():
        logger.info(f"Processing document with key: {key}")
        
        try:
            doc = Document.from_file(**data)
            logger.debug(f"Document '{key}' initialized successfully.")
        
            txn.put(key.encode(), doc.encode())
            logger.debug(f"Document '{key}' added to database.")
            
            logger.info(f"Document '{key}' processed successfully.")
            added_docs += 1

        except Exception as exception:
            logger.error(f"Skipping document '{key}'. An error occurred: '{exception}'.")

        finally:
            total += 1

    logger.warning(f"Done: {added_docs}/{total} document(s) successfully added to the database.")
    logger.info(f"Function 'add_documents' completed.")


def built(env, hash_table, logger):
    logger.info(f"Function 'built' called.")
    
    cleaned_hash_table = clean_table(raw_hash_table, logger)

    polux24 = env.open_db(b"polux24")
    logger.debug(f"Database 'polux24' opened.")
    
    with env.open(write=True, db=polux24) as txn:
        logger.debug(f"New transaction to 'polux24' initialized.")
        add_documents(txn, cleaned_hash_table, logger)

    logger.info(f"Function 'built' completed.")


def main():
    logger = new_logger(__file__, PATH.CACHE)

    with open(PATH.HASH_TABLE, "r", encoding="utf-8") as file:
        hash_table = json.load(file)

    with lmdb.open(PATH.CORPUS_PATH, map_size=VARS.MAP_SIZE) as env:
        built(env, hash_table, logger)

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
