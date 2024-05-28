import configparser
import logging
import socket as sct
import os
import threading

import colorlog

from business.services.cytoscape import Cytoscape
from business.services.transfer import Transfer
from presentation.handler import Handler


def new_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(white)s%(asctime)s %(white)sSERVER: %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s ',
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


def clean_work_dir_after_fail(logger):
    work_dir = os.getcwd()
    logger.info(f'working dir {work_dir}')

    for filename in os.listdir(work_dir):
        if 'GRAPH' in filename or 'STYLES' in filename:
            file_path = os.path.join(work_dir, filename)
            os.remove(file_path)


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

    socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(listeners_amount)

    # services
    transfer = Transfer(logger)
    cytoscape = Cytoscape(logger)

    # handler
    handler = Handler(transfer, cytoscape, logger)

    logger.info('run app')

    conn_status = handler.cytoscape.ping_cs()
    if not conn_status:
        handler.logger.warning("You can't continue work with app until fix cytoscape connection error")
    else:
        handler.logger.info("App successfully connect to Cytoscape")

    while True:

        try:
            conn, address = socket.accept()
            logger.info("accept connection from: " + str(address))
            timeout_seconds = 60
            conn.settimeout(timeout_seconds)

        except BaseException as e:
            logger.error(f'accepting connection: {e}')

        else:
            try:
                handler.conn = conn
                # handler.handle()
                thread = threading.Thread(target=handler.handle)
                thread.start()

            except BaseException as e:
                logger.error(f'handling connection request: {e}')
                handler.conn.close()
                clean_work_dir_after_fail(logger)
