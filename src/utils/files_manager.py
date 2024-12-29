import csv

class FileManager:
    @classmethod
    def create(dir_path, table_header, logger_verbose=True, logger_base_level=logging.DEBUG):
        uuid = generate_uuid()

        self.path.root = os.path.join(dir_path, uuid)
        self.path.files = os.path.join(root, "files")
        self.path.htable = os.path.join(root, "hashes_table.csv")
        self.path.log = os.path.join(root, "main.log")

        table = [[cell.upper() for cell in table_header]]
        logger = create_logger(uiid, log, verbose=logger_verbose, base_level=logger_base_level)

        
        
