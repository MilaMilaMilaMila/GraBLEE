import socket
import configparser
from datetime import datetime
import networkx as nx
import os
import matplotlib.pyplot as plt


def send_nx_graph_to_cytoscape_server(self, client_socket, cs_session_name=None):
    if cs_session_name is None:
        cs_session_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
    gml_graph_filename = cs_session_name + ".gml"
    nx.write_gml(self, gml_graph_filename)
    # nx.write_graphml_xml(self, gml_graph_filename)
    file = open(gml_graph_filename, "rb")
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

    # os.remove(gml_graph_filename)


def get_cytoscape_session(client_socket, cs_session_name=None):
    if cs_session_name is None:
        cs_session_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.cys'
    else:
        cs_session_name += '.cys'

    file = open(cs_session_name, "wb")

    cys_file_len = int.from_bytes(client_socket.recv(1024), byteorder='big')
    print(cys_file_len)
    file_part_len = 1024
    received_data_len = 0
    while True:
        cys_file_data = client_socket.recv(file_part_len)
        if not cys_file_data:
            break
        file.write(cys_file_data)
        received_data_len += len(cys_file_data)
    print(f'get bytes: {received_data_len}')

    file.close()
    # client_socket.send('get session'.encode())
    # answ = client_socket.recv(1024).decode()
    # print(f'server status: {answ}')


def apply_layout(graph, algo_name):
    pos = {}
    match algo_name:
        case 'spring':
            pos = nx.spring_layout(graph)
        case 'shell':
            pos = nx.shell_layout(graph)
        case 'circular':
            pos = nx.circular_layout(graph)
            print('here')
        case 'random':
            pos = nx.random_layout(graph)

    for i in pos:
        pos[i] = (round(pos[i][0], 5), round(pos[i][1], 5))

    nx.set_node_attributes(graph, pos, 'pos')
    nx.draw(graph, pos)
    plt.show()


def client_program(self, cs_session_name=None, layout_algorith='random'):

    config = configparser.ConfigParser()
    config.read('CytoscapeClient/config_client.ini')
    host = config['DEFAULT']['Host']
    port = int(config['DEFAULT']['Port'])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    apply_layout(self, layout_algorith)
    send_nx_graph_to_cytoscape_server(self, client_socket, cs_session_name)
    get_cytoscape_session(client_socket, cs_session_name)

    client_socket.close()


def init_cytoscape_extension():
    nx.Graph.to_cytoscape_session = client_program
