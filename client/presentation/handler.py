import os
from datetime import datetime
from logging import Logger
from socket import socket

import networkx as nx

from client.business.services.nx import Networkx
from client.business.services.transfer import Transfer


class Handler:
    def __init__(self, t: Transfer, n: Networkx, l: Logger, conn: socket = None):
        self.transfer = t
        self.networkx = n
        self.conn = conn
        self.logger = l

    def complete_cyjs_from_graph(self, g: nx.Graph, layout_algo='random'):
        return self.networkx.complete_graph_as_cyjs(g, layout_algo=layout_algo)

    def send_graph(self, file_path: str):
        self.logger.info('start sending graph cyjs data')
        zip_file_path = self.transfer.zip(file_path)
        self.transfer.send_data(self.conn, zip_file_path)
        os.remove(file_path)
        os.remove(zip_file_path)
        self.logger.info('finish sending graph cyjs data')

    def send_styles(self, file_path: str):
        self.logger.info('start sending styles data')
        zip_file_path = self.transfer.zip(file_path)
        self.transfer.send_data(self.conn, zip_file_path)
        os.remove(zip_file_path)
        self.logger.info('finish sending styles data')

    def send_styles_status(self, with_styles):
        self.logger.info('start sending styles status data')
        self.transfer.send_styles_status_data(self.conn, with_styles)
        self.logger.info(f'status: {with_styles}')
        self.logger.info('finish sending styles status data')

    def get_cytoscape_session(self, zip_session_file_name):
        self.logger.info('start getting session data')

        if zip_session_file_name is None:
            zip_session_file_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.cys.zip'
        else:
            zip_session_file_name += '.cys.zip'

        self.transfer.get_data(self.conn, zip_session_file_name)
        session_file_name = self.transfer.unzip(zip_session_file_name)
        os.remove(zip_session_file_name)
        self.logger.info(f'write session in {session_file_name}')
        self.logger.info('finish getting session data')

    def handle(self, g: nx.Graph, cs_session_name=None, styles_filename=None, layout_algo='random'):
        cytoscape_connection_status = self.transfer.get_cytoscape_connection_status(self.conn)
        if not cytoscape_connection_status:
            self.logger.error("Cannot find local or remote Cytoscape. Start Cytoscape and then proceed.")
            return

        styles_status = 0
        if styles_filename:
            styles_status = 1
        self.send_styles_status(styles_status)

        file_path = self.complete_cyjs_from_graph(g, layout_algo)
        try:
            self.send_graph(file_path)
        except BaseException as e:
            self.logger.error(f'sending graph: {e}')
            os.remove(file_path)

        if styles_status:
            self.send_styles(styles_filename)

        self.get_cytoscape_session(cs_session_name)
