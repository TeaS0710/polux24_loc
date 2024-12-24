import glob
import lmdb

from os import basename, splitext

from utils import Document


def built(db_path, hash_table, src_files_dir, logger):
    logger.info("Function 'built' called.")
    
    added_docs, total_files, total_hashes = 0, 0, len(hash_table)

    logger.debug("Opening LMDB environment.")
    
    env = lmdb.open(db_path, map_size=10485760)
    polux24 = env.open_db(b"polux24")
    
    logger.debug(f"Database 'polux24' successfully opened in LMDB environment at '{db_path}'.")
    
    with env.begin(write=True) as txn:
        logger.debug("Transaction opened in write mode.")
    
        txn.drop(polux24, delete=False)
        logger.debug("Database 'polux24' cleared for rewriting.")

        for path in glob.iglob(f"{src_files_dir}/**"):
            logger.info(f"Processing file: {path}")
            key, ext = splitext(basename(path))
            total_files += 1

            if key not in hash_table:
                logger.error(f"Skipping document '{key}'. No entry found in hash table.")
                continue

            if ext not in Document.supported_exts:
                logger.error(f"Skipping document '{key}'. Unsupported extension: '{ext}'.")
                continue

            try:
                doc = Document.from_file(**hash_table[key], path=path)
                logger.debug(f"Document '{key}' initialized successfully.")
                
                txn.put(key.encode(), doc.encode(), db=polux24)
                logger.debug(f"Document '{key}' added to 'polux24' database.")
                
                logger.info(f"Document '{key}' processed successfully.")
                added_docs += 1

            except Exception as exception:
                logger.error(f"Skipping document '{key}'. An error occurred: '{exception}'.")

        logger.warning(f"Processing complete: {added_docs} document(s) successfully added to the database.")
        
        if total_files != added_docs:
            logger.warning(f"Mismatch between added document(s) and file(s): {added_docs} added document(s) vs {total_files} file(s).")
        
        if total_hashes != total_files:
            logger.warning(f"Mismatch between hash(es) and file(s): {total_hashes} hash(es) vs {total_files} file(s).")

    env.close()
    logger.debug("Closing LMDB environment.")
    logger.info("Function 'built' completed successfully.")
