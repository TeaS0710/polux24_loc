import logging

from hashlib import sha256
from uuid import uuid4


def generate_uuid():
    """
    Generates a random unique identifier as a string.
    
    Related objects:
    - :mod: `uuid`
    - :func: `uuid.uuid4`
    
    :returns: The random unique identifier as a string.
    :rtype: str
    """
    
    # Calls `uuid4` from the `uuid` library to obtain a random unique identifier
    # Returns the string representation of it
    return str(uuid4())


def hash_file(path, chunk_size=8192):
    """
    Computes the hash of a file.
    
    Computes the SHA-256 hash of a file binary content, chunk by chunk.
    The segmented implementation helps handle large files and prevents memory overflows.
    Typical use cases include verifying file integrity or detecting modifications.
    
    .. warning::
        This function does not check for the existence of the file before attempting to read it.
        It may raise an IO error.

    Related objects:
    - :mod: `hashlib`
    - :func: `hashlib.sha256`
    - :fund: `hash_str`

    :param path: Path of the file to hash.
    :param chunk_size: Chunk size expressed in bytes.
    :returns: Computed SHA-256 hash as a hexadecimal string.
    
    :type path: str
    :type chunk_size: int
    :rtype: str
    
    :default chunk_size: 8192
    """
    
    # Initializes the hashing function
    hash_func = sha256()
    
    # Opens the file in binary mode
    with open(path, "rb") as file:
        
        # Apply the hashing function chunk by chunk
        while chunk := file.read(chunk_size):
            hash_func.update(chunk)
    
    # Returns the hexadecimal string representation of the result
    return hash_func.hexdigest()


def hash_str(string, encoding="utf-8"):
    """
    Computes the hash of a string.
    
    Computes the SHA-256 hash of the provided string.
    Unlike :func:`hash_file`, the hash is calculated on the entire data at once rather than chunk by chunk.
    Indeed, the function operates directly on data stored in RAM, not read from ROM, so it is unnecessary to prevent memory overflow errors.
    
    Related objects:
    - :mod: `hashlib`
    - :func: `hashlib.sha256`
    - :fund: `hash_file`

    :param string: String to hash.
    :param encoding: Encoding of the string to hash.
    :returns: Computed SHA-256 hash as a hexadecimal string.
    
    :type string: str
    :type encoding: str
    :rtype: str
    
    :default encoding: "utf-8"
    """
    
    # Computes the SHA-256 hash of the string directly, without needing the `.update` method.
    # This approach does not require the initialization of the hashing function (unlike in `hash_file`, see line `hash_func = sha256()` above).
    return sha256(string.encode(encoding)).hexdigest()


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
