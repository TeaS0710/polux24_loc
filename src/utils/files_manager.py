from io import BytesIO, StringIO
import os
import pandas
import shutil

from .misc import hash_data, hash_file


class FileManager:
    def __new__(cls, path, mode, scheme, logger):
        if mode == "r":
            return FileManagerReader(path, scheme, logger)
            
        elif mode == "w":
            return FileManagerWriter(path, scheme, logger, overwrite=False)
            
        elif mode == "w+":
            return FileManagerWriter(path, scheme, logger, overwrite=True)
            
        else:
            logger.critical()
            raise ValueError()

    def __contains__(self, file_hash):
        return file_hash in self.table.index

    def abspath(self, file_hash):
        return os.path.abspath(os.path.join(self.path, "files", file_hash))


class FileManagerReader(FileManager):        
    def __init__(self, path, scheme, logger):
        logger.debug()
        if not os.path.exists(path):
            logger.critical()
            raise FileNotFoundError()

        table_path = os.path.join(path, "table.csv")
        files_path = os.path.join(path, "files")

        logger.debug()
        if not os.path.exists(hashes_table_path):
            logger.critical()
            raise FileNotFoundError()

        logger.debug()
        if not os.path.exists(files_path):
            logger.critical()
            raise FileNotFoundError()

        # Vérifie que scheme est de la forme {str: callable Any vers bool}
        
        try:
            logger.debug()
            dataframe = pandas.read_csv(csv_path)
            
        except Exception as exception:
            logger.critical()
            raise exception

        # Vérifie une correspondance exacte scheme/colone
        
        logger.debug()

        self.root_path = root_path
        self.table_path = table_path
        self.files_path = files_path
        
        self.table = dataframe
        self.invalid = set()
        
    def __post_init__(self):
        # Vérifie la validité des données dans le df
        all_hashes = set(self.table.index)
        table_bool = pandas.DataFrame({
            col: self.table[col].apply(function)
            for col, function in scheme.items()
        })
        invalid_hashes = table_bool[~table_bool.all(axis=1)].index

        # Verifie la validité des fichiers et récupère l'ensemble des fichiers
        all_files = set()
        invalid_files = set()
        for entry in os.scandir(self.files_path):
            all_files.add(entry.name)
            if entry.name != hash_file(entry.path):
                invalid_files.add(entry.name)

        # Identifie les mismatch entre table et fichiers
        extra_hashes = all_hashes - all_files
        missing_hashes = all_files - all_hashes

        # Logs les hashes concernés et nettoie la table des hashes
        if invalid_hashes:
            self.logger.error()
            self.table.drop(invalid_hashes, inplace=True)
            self.invalid |= invalid_hashes

        if invalid_files:
            self.logger.error()
            self.table.drop(invalid_files, errors="ignore", inplace=True)
            self.invalid |= invalid_files

        if extra_hashes:
            self.logger.error()
            self.table.drop(extra_hashes, inplace=True)
            self.invalid |= extra_hashes

        if missing_hashes:
            self.logger.error()
            self.invalid |= missing_hashes

    def __iter__(self):
        for file_hash, file_metadata in self.table:
            yield file_hash, file_metadata.to_dict()
    
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
    def __init__(self, path, logger, scheme=None, overwrite = False):
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
        self.table.to_csv(self.table_path)
    
    def write(content, metadata, binary=False, encoding="utf-8", newline=None, buffering=-1):
        file_hash = hash_sha256(content, binary=binary, encoding=encoding)

        if file_hash in self:
            logger.error()
            return False

        ...

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
