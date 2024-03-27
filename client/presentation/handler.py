from client.business.services.transfer import Transfer
from client.business.services.nx import Networkx
from socket import socket
from logging import Logger
import networkx as nx
from datetime import datetime
import os
from client.data_access.file_system import FileSystemRepo


class Handler:
    def __init__(self, t: Transfer, n: Networkx, l: Logger, conn: socket = None):
        self.transfer = t
        self.networkx = n
        self.conn = conn
        self.logger = l

    def complete_cyjs_from_graph(self, g: nx.Graph, layout_algo='random'):
        return self.networkx.complete_graph_as_cyjs(g, layout_algo=layout_algo)

    def send_graph(self, file_path: str):
        self.logger.info('started send graph cyjs data')
        self.transfer.send_data(self.conn, file_path)
        os.remove(file_path)
        self.logger.info('finished send graph cyjs data')

    def send_styles(self, file_path: str):
        self.logger.info('started send styles data')
        self.transfer.send_data(self.conn, file_path)
        self.logger.info('finished send styles data')

    def get_cytoscape_session(self, session_file_name):
        self.logger.info('started get session data')

        if session_file_name is None:
            session_file_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.cys'
        else:
            session_file_name += '.cys'

        self.transfer.get_data(self.conn, session_file_name)
        self.logger.info(f'session written in {session_file_name}')
        self.logger.info('finished get session data')

    def handle(self, g: nx.Graph, cs_session_name=None, styles_filename=None, layout_algo='random'):
        file_path = self.complete_cyjs_from_graph(g, layout_algo)

        self.send_graph(file_path)

        self.send_styles(styles_filename)

        self.get_cytoscape_session(cs_session_name)
