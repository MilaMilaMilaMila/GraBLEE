import os
import zipfile


class FileSystemRepo:
    @staticmethod
    def read_binary(file_path: str) -> bytes:
        file = open(file_path, "rb")
        data = file.read()
        file.close()
        return data

    @staticmethod
    def read(file_path: str) -> str:
        file = open(file_path)
        data = file.read()
        file.close()
        return data

    @staticmethod
    def write_binary(file_path: str, data: bytes):
        file = open(file_path, "ab")
        file.write(data)
        file.close()

    @staticmethod
    def zip(file_name):
        zip_name = file_name + '.zip'
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_name, os.path.basename(file_name))

    @staticmethod
    def unzip(zip_file_name):
        destination_folder = os.getcwd()
        with zipfile.ZipFile(zip_file_name, 'r') as zipf:
            zipf.extractall(path=destination_folder)
