from io import BytesIO, StringIO
import logging
import os
import pandas
import shutil


class FileManager:
    def __new__(cls, path, mode, logger, scheme=None, hash_func=hash_sha256):
        if mode == "r":
            return FileManagerReader(path, logger, scheme=scheme, hash_func=hash_func)
            
        elif mode == "w":
            return FileManagerWriter(path, logger, scheme=scheme, hash_func=hash_func, overwrite=False)
            
        elif mode == "w+":
            return FileManagerWriter(path, logger, scheme=scheme, hash_func=hash_func, overwrite = True)
            
        else:
            logger.critical()
            raise ValueError()

    def __contains__(self, file_hash):
        return file_hash in self.table.index

    def abspath(self, file_hash):
        return os.path.abspath(os.path.join(self.path, "files", file_hash))

    def match_scheme(self, dictionary):
        if self.scheme is None:
            return True

        dictionary_keys = set(dictionary)
        scheme_keys = set(self.scheme)

        common_keys = dictionary_keys & scheme_keys

        missing_keys = scheme_keys - common_keys
        extra_keys = dictionary_keys - common_keys
        invalid_vals = {key for key in common_keys if not self.scheme[key](dictionary[key])}

        rbool = True
        
        if missing_keys:
            self.logger.error()
            rbool = False
            
        if extra_keys:
            self.logger.error()
            rbool = False
            
        if invalid_vals:
            self.logger.error()
            rbool = False
            
        return rbool


class FileManagerReader(FileManager):        
    def __init__(self, path, logger, scheme=None, hash_func=hash_sha256):
        if not os.path.exists(path):
            logger.critical()
            raise FileNotFoundError()

        hashes_table_path = os.path.join(path, "hashes_table.csv")
        files_path = os.path.join(path, "files")
        
        if not os.path.exists(hashes_table_path):
            logger.critical()
            raise FileNotFoundError()

        if not os.path.exists(files_path):
            logger.critical()
            raise FileNotFoundError()

        try:
            dataframe = pandas.read_csv(csv_path)
            logger.debug()
            
        except Exception as exception:
            logger.critical()
            raise exception

        logger.info()

        self.path = path
        self.table = dataframe
        
    def __post_init__(self):
        wrong_files = self.check()

        if self.wrong_files:
            logger.warning()
            self.pop(wrong_files)
    
    def __iter__(self):
        for file_hash, file_metadata in self.table:
            yield file_hash, file_metadata.to_dict()

    def check(self):
        wrong_keys = set()

        for file_hash, file_metadata in self:
            if not self.match_scheme(file_metadata):
                wrong_keys.add(file_hash)

        for file_path in glob.iglob()
            file_name = os.path.basename(file_path)

            if file_name != self.hash_func(file_path):
                self.logger.error()
                wrong_keys.add(file_hash)

        # Vérifie qu'il y a match entre les entrées
        # Retourne l'ensemble des hashes problemmatique

    def pop(self, index_to_drop):
        self.table.drop(index_to_drop)
    
    def open(self, file_hash, binary=False, encoding="utf-8", newline=None, buffering=1):
        file_path = self.abspath(file_hash)
        
        if file_hash not in self:
            logger.error()
            return BytesIO() if binary else StringIO()

        try: 
            if binary:
                return open(file_path, "rb", buffering=buffering)
                
            else:
                return open(file_path, "r", encoding=encoding, newline=newline, buffering=buffering)

        except Exception as exception:
            logger.error()
            return BytesIO() if binary else StringIO()


class FileManagerWriter(FileManager):        
    def __init__(self, path, logger, scheme=None, hash_func=hash_sha256, overwrite = False):
        if os.path.exists(path):
            if overwrite:
                logger.warning()
                shutil.rmtree(path)
                
            else:
                logger.critical()
                raise PermissionError()

        os.makedirs(path)
        os.makedirs(os.path.join(path, "files"))
        logger.info()
    
        self.path = path
        self.table = pandas.DataFrame()
        self.logger = logger

    def __exit__(self):
        self.logger.info()
        self.table.to_csv(os.path.join(self.path, "hashes_table.csv"))
    
    def write(content, metadata, binary=False, encoding="utf-8", newline=None, buffering=-1):
        file_hash = hash_sha256(content, binary=binary, encoding=encoding)

        if file_hash in self:
            logger.error()
            return False

        if self.check_meta(metadata):
            self.table.loc[file_hash] = metadata

        else:
            return False
        
        try:
            if binary:
                with open(self.abspath(file_hash), "wb", buffering=buffering) as file:
                    file.write(content)
                    return True
                
            else:
                with open(self.abspath(file_hash), "w", encoding=encoding, newline=newline, buffering=buffering) as file:
                    file.write(content)
                    return True
                
        except Exception as exception:
            self.logger.error()
            return False


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
