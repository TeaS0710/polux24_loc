from hashlib import sha256


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

