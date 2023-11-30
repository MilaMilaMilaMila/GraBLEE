import socket
import configparser
from datetime import datetime
import networkx as nx
import os
import matplotlib.pyplot as plt
import json


def set_position_in_cyjs(filename, pos):
    file = open(filename)
    data = json.load(file)
    file.close()
    os.remove(filename)

    for i in data["elements"]["nodes"]:
        i['position'] = {"x": pos[int(i['data']['name'])][0] * 100, "y": pos[int(i['data']['name'])][1] * 100}
        # print(i['position'])

    file = open(f'{filename}.cyjs', 'w')
    json.dump(data, file)
    file.close()


def relabel_nodes_to_str(nx_graph):
    mapping = {}
    for node in nx_graph.nodes:
        mapping[node] = str(node)

    return nx.relabel_nodes(nx_graph, mapping)


def save_graph_as_cytoscape_file(nx_graph, file_format='cyjs', file_name=None, layout_algorithm='random'):
    pos = apply_layout(nx_graph, layout_algorithm)

    # if file name wasn't specified, file name created with current datetime info nx_graph_{date and time}
    if file_name is None:
        file_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'

    # create file in default(gml) or selected format
    full_file_name = f'{file_name}.{file_format}'
    match file_format:
        case 'gml':
            nx.write_gml(nx_graph, full_file_name)
        case 'cyjs':
            str_nodes_nx_graph = relabel_nodes_to_str(nx_graph)
            cyjs_graph_data = nx.cytoscape_data(str_nodes_nx_graph)
            cyjs_file = open(file_name, 'w')
            json.dump(cyjs_graph_data, cyjs_file)
            cyjs_file.close()
            set_position_in_cyjs(file_name, pos)

    # return full file name for import file in cytoscape as network
    return full_file_name


def send_nx_graph_to_cytoscape_server(self, client_socket, cs_session_name=None, layout_algorithm='random'):
    graph_filename = save_graph_as_cytoscape_file(self, file_format='cyjs', file_name=cs_session_name, layout_algorithm=layout_algorithm)
    file = open(graph_filename, "rb")
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

    os.remove(graph_filename)


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

    return pos


def client_program(self, cs_session_name=None, layout_algorith='random'):

    config = configparser.ConfigParser()
    config.read('CytoscapeClient/config_client.ini')
    host = config['DEFAULT']['Host']
    port = int(config['DEFAULT']['Port'])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    send_nx_graph_to_cytoscape_server(self, client_socket, cs_session_name, layout_algorith)
    get_cytoscape_session(client_socket, cs_session_name)

    client_socket.close()


def init_cytoscape_extension():
    nx.Graph.to_cytoscape_session = client_program
