import os

from server.business.services.transfer import Transfer
from server.business.services.cytoscape import Cytoscape
from server.business.models.datadto import DataDTO
from server.business.models.session import Session
from socket import socket
from logging import Logger


class Handler:
    def __init__(self, t: Transfer, c: Cytoscape, l: Logger, conn: socket = None):
        self.transfer = t
        self.cytoscape = c
        self.conn = conn
        self.logger = l

    def get_graph(self) -> DataDTO:
        self.logger.info('started save graph data')

        dto = DataDTO(object_type='GRAPH', file_format='cyjs')
        dto = self.transfer.get_data(self.conn, dto)
        self.logger.info(f'graph data saved in {dto.file_path}')

        self.logger.info('finished save graph data')

        return dto

    def get_styles(self) -> DataDTO:
        self.logger.info('started save styles data')

        dto = DataDTO(object_type='STYLES', file_format='xml')
        dto = self.transfer.get_data(self.conn, dto)
        self.logger.info(f'styles data saved in {dto.file_path}')

        self.logger.info('finished save styles data')

        return dto

    def create_cytoscape_session(self, cys: Session) -> Session:
        self.logger.info('started create cytoscape session')

        cys = self.cytoscape.create_cytoscape_session(cys)

        self.logger.info('finished create cytoscape session')

        return cys

    def send_cytoscape_session(self, cys: Session):
        self.logger.info('started send cytoscape session')

        self.transfer.send_data(self.conn, f'{cys.session_name}.cys')

        self.logger.info('finished send cytoscape session')

    def clean_work_dir(self, graph_dto: DataDTO, styles_dto: DataDTO, cys: Session):
        os.remove(graph_dto.file_path)
        os.remove(styles_dto.file_path)
        os.remove(cys.session_path)

    def handle(self):
        cys = Session()

        graph_dto = self.get_graph()
        cys.graph_file_path = graph_dto.file_path

        styles_dto = self.get_styles()
        cys.styles_name = styles_dto.file_name
        cys.styles_file_path = styles_dto.file_path

        cys = self.create_cytoscape_session(cys)
        self.send_cytoscape_session(cys)

        self.clean_work_dir(graph_dto, styles_dto, cys)
