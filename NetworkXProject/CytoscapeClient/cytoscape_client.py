import socket
import configparser
from datetime import datetime
import os


def send_nx_graph_to_cytoscape_server(client_socket):
    filename = 'test_graph.gml'
    file = open(filename, "rb")
    data = file.read()
    file.close()
    len_data_in_bytes = len(data).to_bytes(length=8, byteorder='big')
    client_socket.send(len_data_in_bytes)
    # get_file_size = client_socket.recv(1024).decode()
    # print(get_file_size)
    client_socket.send(data)
    # data = client_socket.recv(1024).decode()
    # print(data)
    # data = client_socket.recv(1024).decode()
    # print(data)

    # os.remove(filename)


def get_cytoscape_session(client_socket, cys_file_name=None):
    cys_file_len = int.from_bytes(client_socket.recv(1024), byteorder='big')
    cys_file_data = client_socket.recv(cys_file_len)
    if cys_file_name is None:
        cys_file_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.cys'
    file = open(cys_file_name, "wb")
    file.write(cys_file_data)
    file.close()
    client_socket.send('get session'.encode())
    answ = client_socket.recv(1024).decode()
    print(f'server status: {answ}')


def client_program():
    config = configparser.ConfigParser()
    config.read('config_client.ini')

    host = config['REMOTE']['Host']
    port = int(config['REMOTE']['Port'])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    send_nx_graph_to_cytoscape_server(client_socket)
    get_cytoscape_session(client_socket)

    client_socket.close()


if __name__ == '__main__':
    client_program()
