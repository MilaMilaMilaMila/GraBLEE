import logging
import socket as sct
import configparser
from pathlib import Path

import colorlog
import networkx as nx

from client.business.services.nx import Networkx
from client.business.services.transfer import Transfer
from client.presentation.handler import Handler


def init_cytoscape_extension():
    nx.Graph.to_cytoscape_session = main


def new_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(white)s%(asctime)s %(white)sCLIENT: %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'black,bg_red',
        },
        secondary_log_colors={},
        style='%'
    ))

    logger = colorlog.getLogger('example')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


def main(self, cs_session_name=None, layout_algo=None, styles_filename=None):
    # define logger
    logger = new_logger()

    # config
    config = configparser.ConfigParser()

    current_file = Path(__file__).resolve()
    container_dir = current_file.parent
    config_path = container_dir / 'business' / 'config' / 'config.ini'
    config.read(config_path)

    # define connection
    connection_params = "CONNECTION_PARAMS"

    host = config[connection_params]['host']
    port = int(config[connection_params]['port'])
    timeout_seconds = int(config[connection_params]['timeout_seconds'])

    logger.info(f'define host {host}')
    logger.info(f'define port {port}')

    socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
    socket.settimeout(timeout_seconds)
    socket.connect((host, port))

    # services
    transfer = Transfer(logger)
    nx = Networkx(logger)

    # handler
    handler = Handler(transfer, nx, logger, socket)

    logger.info('run app')

    try:
        handler.handle(g=self,
                       cs_session_name=cs_session_name,
                       layout_algo=layout_algo,
                       styles_filename=styles_filename)
    except BaseException as e:
        logger.error(f'handling request: {e}')

    socket.close()
