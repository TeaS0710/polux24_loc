from io import BytesIO, StringIO
import logging
import os
import pandas


class FileManager:
    @staticmethod
    def fake_stream(*args, **kwargs):
        mode = open_kwargs.get("mode", open_args[0] if open_args else "r")

        if "b" in mode:
            return BytesIO(*args, **kwargs)

        else:
            return StringIO(*args, **kwargs)
    
    @classmethod 
    def __new__(cls, path, mode, logger):
        if mode == "r":
            return cls.Reader(path, logger)
            
        elif mode == "w":
            return cls.Writer(path, logger, overwrite=False)
            
        elif mode == "w+":
            return cls.Writer(path, logger, overwrite = True)
            
        else:
            logger.critical(f"")
            raise ValueError()

    def __enter__(self):
        return self

    def __exit__(self):
        del self

    def abspath(self, file_hash):
        if file_hash not in self:
            return ""

        return os.path.abspath(f"{self.path}{os.sep}files{os.sep}{file_hash}")

    def __contains__(self, file_hash):
        return file_hash in self.table

    class Reader(FileManager):
        def __init__(self, path, logger):
            """
            # Si path n'existe pas
    			logger.critical
    			raise FileNotFound
    		
    		# Si path ne contient pas hashes_table.json
    			logger.critical
    			raise FileNotFound
    		
    		# Si path ne contient pas files/
    			logger.critical
    			raise FileNotFound
    		
    		# Si hashes_table.csv est pas chargeable en DF
    			logger.critical
    			raise l'erreur levée par pd
    		
    		# Fait les vérifications de types et valeur nécéssaires sur les données de table
    			logger.error()
    			ajoute la hash dans la liste à retirer
    		
    		# vérifie que sous `files/` chaque fichier est nommé d'après son hash
    			logger.error()
    			ajoute le hash dans la liste à retirer
    		
    		# vérifie la correspondance entre les entrées de `files/` et de la table
    			logger.error()
    			ajoute les hashs concernés dans la liste à retirer
    		
    		# Filtre la table en retirant les hashs buggés
            """
            self.path = path
            self.table = table

        """
        Itère sur file_hash, file_meta in instance
        """
        
        def __iter__(self):
            pass

        def __next__(self):
            pass
                      
        def open(self, file_hash, encoding="utf-8", newline="\n", buffering=1):
            if (file_path := self.abspath(file_hash)) is None:
                logger.error()
                return StringIO()

            return open(file_path, "r", encoding=encoding, newline=newline, buffering=buffering)

        def openb(self, file_hash, buffering=-1):
            if (file_path := self.abspath(file_hash)) is None:
                logger.error()
                return BytesIO()

            return open(file_path, "rb", buffering=buffering)

    class Writer(FileManager):
        def __init__(self, path, logger, overwrite = False):
            pass

        def write(self, content, data):
            pass


def create_logger(name, path, verbose=False, level=logging.INFO):
    """
    Creates and configures a logger.
    
    Creates a logger and sets its minimum degree of severity to `level`.
    Adds a handler to `path`, and if `verbose` is True, a console handler.
    Logs an INFO message throught the logger, displaying its name and the path of the current Python script.
    Returns the configured logger.

    Related objects:
    - :mod: `logging`
    - :func: `logging.getLogger`
    - :class: `logging.Logger`
    - :class: `logging.Formatter`
    - :class: `logging.FileHandler`
    - :class: `logging.StreamHandler`

    :param name: Unique identifier for the logger object, used to distinguish it from others.
    :param path: Path to write the log file.
    :param verbose: Boolean flag to control the addition of a second handler for console output.
    :param level: Minimal severity level of log entries.
    :returns: Configured logger instance.
    
    :type name: str
    :type path: str
    :type verbose: bool
    :type level: int
    :rtype: logging.Logger
    
    :default verbose: False
    :default level: logging.INFO
    """
    
    # Creates a logger instance with the specified name and log level
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Creates a formatter for log entries
    formatter = logging.Formatter("%(asctime)s.%(msecs)03d -- %(name)s -- %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")

    # Creates a file handler to `path` and applies `formatter` to it
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    
    # Adds it to the logger
    logger.addHandler(file_handler)

    # If `verbose` is True, adds a second handler to display log entries in console
    if verbose:
        
        # Creates a stream handler to stdout and applies `formatter` to it
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Adds it to the logger
        logger.addHandler(console_handler)

    # Logs an initial info-level message with the logger's name and the Python script path
    logger.info(f"Logger '{name}' initialized for logging the execution of script '{__file__}'")

    # Returns the configured logger instance
    return logger
