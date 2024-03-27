import networkx as nx
import json

class FileSystemRepo:
    @staticmethod
    def read_binary(file_path: str) -> bytes:
        file = open(file_path, "rb")
        data = file.read()
        file.close()
        return data

    @staticmethod
    def write_binary(file_path: str, data: bytes):
        file = open(file_path, "ab")
        file.write(data)
        file.close()

    @staticmethod
    def write_cyjs(file_path: str, data: dict):
        file = open(file_path, 'w')
        json.dump(data, file)
        file.close()
