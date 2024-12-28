def db_explorer(txn, data_wrapper, logger):
    logger.info("Function 'db_explorer' called.")
    total, yielded = 0, 0
  
    cursor = txn.cursor()
    logger.debug("Cursor initialized, starting traversal.")
  
    for bin_key, bin_val in cursor:
        key = bin_key.decode()
        logger.debug(f"Attempting to decode document '{key}'.")

        try:
            val = data_wrapper.decode(bin_val)
            logger.info(f"Document '{key}' decoded successfully.")

            yield key, val
            yielded += 1
            logger.debug(f"Document '{key}' yielded. Total yielded: {yielded}.")
        
        except Exception as exception:
            logger.error(f"Failed to decode document '{key}': {exception}")
        
        finally:
            total += 1
            logger.debug(f"Moving to the next document. Processed so far: {total}.")

    logger.warning(f"Done. {yielded} documents decoded out of {total}.")
    logger.info("Process completed.")
