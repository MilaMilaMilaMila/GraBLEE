import configparser
import logging
import socket as sct
import os
import threading

import colorlog

from business.services.cytoscape import Cytoscape
from business.services.transfer import Transfer
from presentation.handler import Handler


def new_logger(address):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        f'%(white)s%(asctime)s %(purple)s{address} %(white)sSERVER: %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s ',
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

    logger = colorlog.getLogger(address)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


def delete_logger(logger):
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logging.Logger.manager.loggerDict.pop(logger.name)


def clean_work_dir_after_fail(logger):
    work_dir = os.getcwd()
    logger.info(f'working dir {work_dir}')

    for filename in os.listdir(work_dir):
        if 'GRAPH' in filename or 'STYLES' in filename:
            file_path = os.path.join(work_dir, filename)
            os.remove(file_path)


def handle(host_address, conn, lock):
    try:
        cur_connection_logger = new_logger(host_address)
        cur_connection_transfer = Transfer(cur_connection_logger)
        cur_connection_cytoscape = Cytoscape(cur_connection_logger)
        cur_connection_handler = Handler(cur_connection_transfer, cur_connection_cytoscape, cur_connection_logger, lock)

        cur_connection_handler.conn = conn
        cur_connection_handler.handle()
    except sct.error as e:
        logger.error(f'handling connection {address[0]} request: {e}')
        handler.conn.close()
        # TODO clean_work_dir_after_fail(logger) как-то это сделать
    finally:
        if 'cur_connection_logger' in locals():
            delete_logger(cur_connection_logger)


if __name__ == '__main__':
    # logger
    logger = new_logger('127.0.0.1')

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

    # mutex
    lock = threading.Lock()

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

        except sct.error as e:
            logger.error(f'accepting connection: {e}')

        else:
            thread = threading.Thread(target=handle, args=(address[0], conn, lock))
            thread.start()
