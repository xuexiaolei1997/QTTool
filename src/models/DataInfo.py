import os
import uuid
import chardet

class DataInfo:
    def __init__(self, file_path: str) -> None:
        self.file_id = str(uuid.uuid4()).replace('-', '')
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_data = None
        self.file_info = os.stat(file_path)
        self.file_size = self.file_info.st_size * 8 / 1024 / 1024

        # Ensure encoding type
        with open(file_path, 'rb') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
        self.encoding = encoding