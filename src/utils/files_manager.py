import logging
import os
import pandas


class FileManager:
    @classmethod 
    def __new__(cls, path, mode, logger):
        if mode == "r":
            return cls.Reader(path, logger)
        elif mode == "w":
            return cls.Writer(path, logger, overwrite=False)
        elif mode == "w+":
            return cls.Writer(path, logger, overwrite = True)
        else:
            logger.critical(f"Nike ta mere")
            raise ValueError 

    class Reader(FileManager):
        Def __init__(self, path, logger):
            pass

    class Writer(FileManager):
        Def __init__(self, path, logger, overwrite = False):
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
        
