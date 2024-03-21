import configparser
import logging
import colorlog
from server.business.services.transfer import Transfer
from server.business.services.cytoscape import Cytoscape
from server.presentation.handler import Handler
import socket as sct


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

    logger.info(f'defined host {host}')
    logger.info(f'defined port {port}')
    logger.info(f'defined listeners_amount {listeners_amount}')

    socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(listeners_amount)

    # services
    transfer = Transfer(logger)
    cytoscape = Cytoscape(logger)

    # handler
    handler = Handler(transfer, cytoscape, logger)

    logger.info('app run')
    while True:
        conn, address = socket.accept()
        logger.info("accepted connection from: " + str(address))

        handler.conn = conn
        handler.handle()

