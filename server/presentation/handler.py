import os
from logging import Logger
from socket import socket
import threading

from business.models.datadto import DataDTO
from business.models.session import Session
from business.services.cytoscape import Cytoscape
from business.services.transfer import Transfer


class Handler:
    def __init__(self, t: Transfer, c: Cytoscape, l: Logger, lock: threading.Lock, conn: socket = None):
        self.transfer = t
        self.cytoscape = c
        self.conn = conn
        self.logger = l
        self.lock = lock

    def get_styles_status_data(self):
        self.logger.info('start saving content info data')

        styles_status = self.transfer.get_data()

        self.logger.info('finish saving content info data')

        return styles_status

    def get_graph(self) -> DataDTO:
        self.logger.info('start saving graph data')

        dto = DataDTO(object_type='GRAPH', file_format='cyjs')
        zip_dto = DataDTO(object_type='GRAPH', file_format='cyjs.zip')
        zip_dto = self.transfer.get_data(self.conn, zip_dto)
        self.logger.info(f'archived graph data saved in {zip_dto.file_path}')
        dto_file_name = self.transfer.unzip(zip_dto.file_path)
        dto.file_name = zip_dto.file_name
        dto.file_path = f'{dto.file_name}.{dto.file_format}'
        self.logger.info(f'graph data saved in {dto.file_path}')
        self.logger.info('finish saving graph data')

        return dto

    def get_styles(self) -> DataDTO:
        self.logger.info('start saving styles data')

        dto = DataDTO(object_type='STYLES', file_format='xml')
        zip_dto = DataDTO(object_type='STYLES', file_format='xml.zip')
        zip_dto = self.transfer.get_data(self.conn, zip_dto)
        self.logger.info(f'archived styles data saved in {zip_dto.file_path}')
        dto_file_name = self.transfer.unzip(zip_dto.file_path)
        dto.file_name = zip_dto.file_name
        dto.file_path = f'{dto.file_name}.{dto.file_format}'
        self.logger.info(f'styles data saved in {dto.file_path}')
        self.logger.info('finish saving styles data')

        return dto

    def create_cytoscape_session(self, cys: Session) -> Session:
        self.logger.info('start creating cytoscape session')

        cys = self.cytoscape.create_cytoscape_session(cys)

        self.logger.info('finish creating cytoscape session')

        return cys

    def send_cytoscape_session(self, cys: Session):
        self.logger.info('start sending cytoscape session')

        zip_session_file_name = self.transfer.zip(f'{cys.session_name}.cys')
        self.transfer.send_data(self.conn, zip_session_file_name)

        self.logger.info('finish sending cytoscape session')

    def clean_work_dir(self, graph_dto: DataDTO, cys: Session, styles_dto=None):
        os.remove(graph_dto.file_path)
        os.remove(f'{graph_dto.file_path}.zip')
        if styles_dto:
            os.remove(styles_dto.file_path)
            os.remove(f'{styles_dto.file_path}.zip')
        os.remove(cys.session_path)
        os.remove(f'{cys.session_path}.zip')

    def get_styles_status(self):
        return self.transfer.get_styles_status_data(self.conn)

    def handle(self):
        conn_status = self.cytoscape.ping_cs()
        if not conn_status:
            self.transfer.send_cytoscape_connection_status(self.conn, status=conn_status)
            return
        else:
            self.transfer.send_cytoscape_connection_status(self.conn, status=conn_status)

        with_styles = self.get_styles_status()

        cys = Session()

        graph_dto = self.get_graph()
        cys.graph_file_path = graph_dto.file_path

        styles_dto = None
        if with_styles != 0:
            styles_dto = self.get_styles()
            cys.styles_name = styles_dto.file_name
            cys.styles_file_path = styles_dto.file_path

        self.lock.acquire()
        cys = self.create_cytoscape_session(cys)
        self.lock.release()

        self.send_cytoscape_session(cys)

        self.clean_work_dir(graph_dto, cys, styles_dto)
