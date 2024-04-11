from datetime import datetime
from logging import Logger
from socket import socket

from business.models.datadto import DataDTO
from data_access.file_system import FileSystemRepo


class Transfer:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.package_size = 1024

    def get_data(self, s: socket, dto: DataDTO) -> DataDTO:
        self.logger.info('execute get data')

    def send_data(self, s: socket, file_path: str):
        self.logger.info('execute send data')
