import lmdb
from os.path import basename, splitext, exists

from utils import Document


def add_documents(txn, hash_table, logger):
    logger.warning("Function 'built' called.")
    
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

    logger.warning(f"Function 'built' completed: {added_docs}/{total} document(s) successfully added to the database.")


def built(db_path, hash_table_path, logger):
    pass
    # Implémenter:
    # Ouvre hash_table_path
    # Ouvre l'env, polux24 et initie la transaction
    # appelle add_documents
