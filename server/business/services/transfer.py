from datetime import datetime
from logging import Logger
from socket import socket
import math

from business.models.datadto import DataDTO
from data_access.file_system import FileSystemRepo


class Transfer:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.package_size = 1024

    def zip(self, file_name) -> str:
        self.logger.info('start archiving file')
        FileSystemRepo.zip(file_name)
        self.logger.info('end archiving file')
        return file_name + '.zip'

    def unzip(self, zip_file_name) -> str:
        self.logger.info('start unpacking file')
        FileSystemRepo.unzip(zip_file_name)
        self.logger.info('end unpacking file')
        return zip_file_name[0:-4]

    def send_cytoscape_connection_status(self, conn: socket, status: int):
        self.logger.info('start sending cytoscape connection status')

        status_bin = status.to_bytes(length=8, byteorder='big')
        conn.send(status_bin)
        self.logger.info(f'status {status} was sent')
        response = conn.recv(self.package_size).decode()
        self.logger.info(f'client response: {response}')

        self.logger.info('finish sending cytoscape connection status')

    def get_data_len(self, conn: socket) -> int:
        self.logger.info('start getting data len')

        data_len = conn.recv(self.package_size)
        data_len = int.from_bytes(data_len, byteorder='big')
        msg = f'receive data len: {data_len}'
        self.logger.info(msg)
        conn.send(msg.encode())

        self.logger.info('finish getting data len')

        return data_len

    def send_data_len(self, conn: socket, data_len: int):
        self.logger.info('start sending data len')
        self.logger.info(f'data len = {data_len}')

        len_data_bin = data_len.to_bytes(length=8, byteorder='big')
        conn.send(len_data_bin)
        response = conn.recv(self.package_size).decode()
        self.logger.info(f'client response: {response}')

        self.logger.info('finish sending data len')

    def get_data(self, conn: socket, dto: DataDTO) -> DataDTO:
        data_len = self.get_data_len(conn)

        self.logger.info('start getting data')

        dto.file_name = f'{dto.object_type}_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
        full_file_name = f'{dto.file_name}.{dto.file_format}'
        dto.file_path = full_file_name

        received_data_len = 0
        batches_amount = int(math.ceil(data_len / self.package_size))
        for i in range(batches_amount):
            try:
                batch = conn.recv(min(self.package_size, data_len - received_data_len))
            except BaseException as e:
                err_msg = f'getting data batch error: {e}'
                conn.send(err_msg.encode())
                self.logger.error(err_msg)
                self.logger.info('app is terminated')
                exit()

            conn.send('ok'.encode())

            FileSystemRepo.write_binary(full_file_name, batch)
            received_data_len += len(batch)

        msg = f'received bytes: {received_data_len}'
        self.logger.info(msg)

        conn.send(msg.encode())

        return dto

    def get_styles_status_data(self, conn: socket):
        self.logger.info('start getting styles status data')
        styles_status = self.get_data_len(conn)
        self.logger.info(f'received status: {styles_status}')
        self.logger.info('finish getting styles status data')

        return styles_status

    def get_layout_status_data(self, conn: socket):
        self.logger.info('start getting layout status data')
        layout_status = self.get_data_len(conn)
        self.logger.info(f'received status: {layout_status}')
        self.logger.info('finish getting layout status data')

        return layout_status

    def send_data(self, conn: socket, file_path: str):
        data = FileSystemRepo.read_binary(file_path)
        data_len = len(data)
        self.send_data_len(conn, data_len)

        self.logger.info('start sending data')

        for i in range(0, data_len, self.package_size):
            conn.send(data[i:min(i + self.package_size, data_len)])
            response = conn.recv(self.package_size).decode()
            # self.logger.debug(f'{response}')

            if response != 'ok':
                self.logger.error('sending data batch error:')
                self.logger.info('app is terminated')
                exit()

        response = conn.recv(self.package_size).decode()
        self.logger.info(f'client response: {response}')

        self.logger.info('finish sending data')
