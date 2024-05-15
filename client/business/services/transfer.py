import configparser
import os
from logging import Logger
from socket import socket

from client.data_access.file_system import FileSystemRepo


class Transfer:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.package_size = 1024

    def get_cytoscape_connection_status(self, conn: socket) -> int:
        self.logger.info('start getting cytoscape connection status')

        status = conn.recv(self.package_size)
        status = int.from_bytes(status, byteorder='big')
        # msg = f'received cytoscape connection status: {status}'
        # self.logger.info(msg)
        # conn.send(msg.encode())

        self.logger.info('finish getting cytoscape connection status')

        return status

    def get_data_len(self, conn: socket) -> int:
        self.logger.info('start getting data len')

        data_len = conn.recv(self.package_size)
        data_len = int.from_bytes(data_len, byteorder='big')
        msg = f'received data len: {data_len}'
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
        self.logger.info(f'server response: {response}')

        self.logger.info('finish sending data len')

    def get_data(self, conn: socket, file_path: str):
        data_len = self.get_data_len(conn)

        self.logger.info('start getting data')

        received_data_len = 0
        while received_data_len < data_len:
            try:
                batch = conn.recv(min(self.package_size, data_len - received_data_len))
                conn.send('ok'.encode())
            except BaseException as e:
                self.logger.error(f'getting data: {e}')
                self.logger.info('app was terminated')
                exit()

            if not batch:
                self.logger.info('finish getting data')
                break

            FileSystemRepo.write_binary(file_path, batch)
            received_data_len += len(batch)

        msg = f'received bytes: {received_data_len}'
        self.logger.info(msg)

        conn.send(msg.encode())

    def send_data(self, conn: socket, file_path: str):
        data = FileSystemRepo.read_binary(file_path)
        data_len = len(data)
        self.send_data_len(conn, data_len)

        self.logger.info('start sending data')

        for i in range(0, data_len, self.package_size):
            conn.send(data[i:min(i + self.package_size, data_len)])
            response = conn.recv(self.package_size).decode()

            if response != 'ok':
                self.logger.error('getting data batch error')
                self.logger.info('app was terminated')
                exit()

        response = conn.recv(self.package_size).decode()
        self.logger.info(f'server response: {response}')

        self.logger.info('finish sending data')
