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
