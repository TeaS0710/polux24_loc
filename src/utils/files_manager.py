from io import BytesIO, StringIO
from logging import Logger

import os
import pandas
import shutil

from .misc import hash_data, hash_file

# Le cas ou on a pas que des fichiers sans nom sous le dir à vérifier

class FileManager:
    def __new__(cls, root_path, mode, scheme, logger):
        if not isinstance(logger, Logger):
            raise TypeError("logger must be an instance of logging.Logger.")

        if not isinstance(root_path, str):
            raise TypeError("root_path must be a string.")

        if not isinstance(mode, str):
            raise TypeError("mode must be a string.")

        if not isinstance(scheme, dict):
            raise TypeError("scheme must be a dict.")

        for key, value in scheme.items():
            if not isinstance(key, str):
                raise TypeError(f"{key} in scheme is not a string.")

            if not callable(value):
                raise TypeError(f"{value} in scheme is not a callable.")

        if mode == "r":
            return FileManagerReader(root_path, scheme, logger)

        elif mode == "w":
            return FileManagerWriter(root_path, scheme, logger, overwrite=False)

        elif mode == "w+":
            return FileManagerWriter(root_path, scheme, logger, overwrite=True)

        else:
            logger.critical(f"Unknown mode: {mode}")
            raise NotImplementedError(f"Unknown mode: {mode}")

    def __contains__(self, file_hash):
        return file_hash in self.table.index

    def abspath(self, file_hash):
        return os.path.abspath(os.path.join(self.files_path, file_hash))


class FileManagerReader(FileManager):
    def __init__(self, root_path, scheme, logger):
        logger.debug(f"Initializing FileManagerReader on {root_path}")
        if not os.path.exists(root_path):
            logger.critical("Root path does not exist")
            raise FileNotFoundError(f"{root_path} does not exist")

        table_path = os.path.join(root_path, "table.csv")
        files_path = os.path.join(root_path, "files")

        logger.debug("Checking if table.csv exists")
        if not os.path.exists(table_path):
            logger.critical("table.csv not found")
            raise FileNotFoundError(f"{table_path} not found")

        logger.debug("Checking if files/ directory exists")
        if not os.path.exists(files_path):
            logger.critical("files directory not found")
            raise FileNotFoundError(f"{files_path} not found")

        try:
            logger.debug("Reading table.csv")
            dataframe = pandas.read_csv(table_path, dtype=str, index_col=0)

        except Exception as exception:
            logger.critical(f"Error reading CSV: {exception}")
            raise exception

        logger.debug("Validating columns in table.csv")
        dataframe_cols = set(dataframe.columns)
        scheme_cols = set(scheme.keys())
        missing_cols = scheme_cols - dataframe_cols
        extra_cols = dataframe_cols - scheme_cols

        if missing_cols and extra_cols:
            logger.critical(f"Missing columns: {missing_cols}, Extra columns: {extra_cols}")
            raise KeyError(f"Missing columns: {missing_cols}, Extra columns: {extra_cols}")

        elif missing_cols:
            logger.critical(f"Missing columns: {missing_cols}")
            raise KeyError(f"Missing columns: {missing_cols}")

        elif extra_cols:
            logger.critical(f"Extra columns: {extra_cols}")
            raise KeyError(f"Extra columns: {extra_cols}")

        self.root_path = root_path
        self.table_path = table_path
        self.files_path = files_path

        self.table = dataframe
        self.logger = logger
        self.scheme = scheme

        self.__post_init__()

    def __post_init__(self):
        all_hashes = set(self.table.index)
        table_bool = {}
        for col, function in self.scheme.items():
            table_bool[col] = self.table[col].apply(function)
        table_bool = pandas.DataFrame(table_bool)

        invalid_hashes = table_bool[~table_bool.all(axis=1)].index

        all_files = set()
        invalid_files = set()
        for entry in os.scandir(self.files_path):
            all_files.add(entry.name)

            if entry.name != hash_file(entry.path):
                invalid_files.add(entry.name)

        extra_hashes = all_hashes - all_files
        missing_hashes = all_files - all_hashes

        if invalid_hashes.any():
            self.logger.error(f"Invalid hashes in table: {list(invalid_hashes)}")
            self.table.drop(invalid_hashes, inplace=True)

        if invalid_files:
            self.logger.error(f"Invalid files in directory: {list(invalid_files)}")
            self.table.drop(invalid_files, errors="ignore", inplace=True)

        if extra_hashes:
            self.logger.error(f"File hashes in table not found in directory: {list(extra_hashes)}")
            self.table.drop(extra_hashes, inplace=True)

        if missing_hashes:
            self.logger.error(f"File hashes in directory not found in table: {list(missing_hashes)}")

    def __iter__(self):
        for file_hash, row in self.table.iterrows():
            yield file_hash, row.to_dict()

    def open(self, file_hash, binary=False, encoding="utf-8", newline=None, buffering=1):
        file_path = self.abspath(file_hash)

        if file_hash not in self:
            self.logger.error(f"Attempt to open unknown file hash: {file_hash}")
            return BytesIO() if binary else StringIO()

        try:
            if binary:
                return open(file_path, "rb", buffering=buffering)

            else:
                return open(file_path, "r", encoding=encoding, newline=newline, buffering=buffering)

        except Exception as exception:
            self.logger.error(f"Error opening file {file_path}: {exception}")
            return BytesIO() if binary else StringIO()


class FileManagerWriter(FileManager):
    def __init__(self, root_path, scheme, logger, overwrite=False):
        if os.path.exists(root_path):
            if overwrite:
                logger.warning(f"Overwriting existing directory {root_path}")
                shutil.rmtree(root_path)
                
            else:
                logger.critical(f"Root path {root_path} already exists and overwrite=False")
                raise PermissionError(f"{root_path} already exists and overwrite=False")

        files_path = os.path.join(root_path, "files")
        table_path = os.path.join(root_path, "table.csv")

        os.makedirs(root_path)
        os.makedirs(files_path)
        logger.info(f"Created directories: {root_path} and {files_path}")

        self.root_path = root_path
        self.table_path = table_path
        self.files_path = files_path

        self.table = pandas.DataFrame()
        self.fields = set(self.scheme.keys())
        self.logger = logger
        self.scheme = scheme

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info(f"Saving table to {self.table_path}")
        self.table.to_csv(self.table_path)

    def write(self, content, metadata, binary=False, encoding="utf-8", newline=None, buffering=-1):
        file_hash = hash_data(content, binary=binary, encoding=encoding)

        if file_hash in self:
            self.logger.error(f"File already exists for hash: {file_hash}.")
            return False

        metadata_keys = set(metadata.keys())
        common_keys = metadata_keys & self.fields

        missing_keys = self.fields - common_keys
        extra_keys = metadata_keys - common_keys
        invalid_vals = {
            key for key in common_keys
            if not self.scheme[key](metadata[key])
        }


        if missing_keys or extra_keys or invalid_vals:
            if missing_keys:
                self.logger.error(f"Metadata validation error. Missing: {missing_keys}.)

            if extra_keys:
                self.logger.error(f"Metadata validation error. Extra: {extra_keys}.)

            if invalid_vals:
                self.logger.error(f"Metadata validation error. Invalid: {invalid_vals}.)

        else:
            return False

        try:
            file_path = self.abspath(file_hash)

            if binary:
                with open(file_path, "wb", buffering=buffering) as file:
                    file.write(content)
            else:
                with open(file_path, "w", encoding=encoding, newline=newline, buffering=buffering) as file:
                    file.write(content)

            self.table.loc[file_hash] = new_row
            return True

        except Exception as exception:
            self.logger.error(f"Error writing file {file_hash}: {exception}")
            return False
