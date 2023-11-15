import socket
import configparser
from datetime import datetime
import os
import json
from dict2xml import dict2xml


def send_nx_graph_to_cytoscape_server(client_socket):
    filename = 'test_graph.gml'
    file = open(filename, "rb")
    data = file.read()
    file.close()
    len_data_in_bytes = len(data).to_bytes(length=8, byteorder='big')
    client_socket.send(len_data_in_bytes)
    get_file_size = client_socket.recv(1024).decode()
    print(get_file_size)
    client_socket.send(data)
    data = client_socket.recv(1024).decode()
    print(data)
    os.remove(filename)


def get_cytoscape_session(client_socket, cys_file_name=None):
    cys_file_len = int.from_bytes(client_socket.recv(1024), byteorder='big')
    cys_file_data = client_socket.recv(cys_file_len)
    if cys_file_name is None:
        cys_file_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.cys'
    file = open(cys_file_name, "wb")
    file.write(cys_file_data)
    file.close()


def send_style_file(client_socket, style_file_path=None):
    file_format = style_file_path.split('.')[-1]
    style_file = open(style_file_path)

    style_data = ""
    if file_format == "json":
        data = json.load(style_file)
        style_data = dict2xml(data)
    elif file_format == "xml":
        style_data = style_file.read()

    bytes_style = bytes(style_data, 'utf-8')
    client_socket.send(bytes_style)


def open_as_cs_session(session_name=None, style_file_path=None):
    config = configparser.ConfigParser()
    config.read('config_client.ini')

    host = config['DEFAULT']['Host']
    port = int(config['DEFAULT']['Port'])

    client_socket = socket.socket()
    client_socket.connect((host, port))

    send_nx_graph_to_cytoscape_server(client_socket)
    get_cytoscape_session(client_socket, cys_file_name=session_name)

    client_socket.close()


if __name__ == '__main__':
    open_as_cs_session()