import configparser
import logging
import socket

import colorlog

from business.services.cytoscape import Cytoscape
from business.services.transfer import Transfer
from presentation.handler import Handler


def new_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(white)sSERVER: %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s',
        datefmt=None,
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


if __name__ == '__main__':
    # logger
    logger = new_logger()

    # config
    config = configparser.ConfigParser()
    config.read('business/config/config.ini')

    # define connection
    connection_params = "CONNECTION_PARAMS"

    host = config[connection_params]['host']
    port = int(config[connection_params]['port'])
    listeners_amount = int(config[connection_params]['listeners_amount'])

    logger.info(f'define host {host}')
    logger.info(f'define port {port}')
    logger.info(f'define listeners_amount {listeners_amount}')

    # services
    transfer = Transfer(logger)
    cytoscape = Cytoscape(logger)

    # handler
    handler = Handler(transfer, cytoscape, logger)

    logger.info('run app')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(listeners_amount)

        conn, address = s.accept()
        logger.info("accept connection from: " + str(address))
        with conn:
            handler.conn = conn
            handler.handle()
