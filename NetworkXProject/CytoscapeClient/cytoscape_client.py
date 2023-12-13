import socket
import configparser
from datetime import datetime
import networkx as nx
import os
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


def send_nx_graph_to_cytoscape_server(self, conn, cs_session_name=None, layout_algorithm='random', package_size=1024):
    print('\nCLIENT: GRAPH DELIVER START')
    graph_filename = save_graph_as_cytoscape_file(self, file_format='cyjs', file_name=cs_session_name, layout_algorithm=layout_algorithm)
    file = open(graph_filename, "rb")
    # TODO читать тоже лучше не полностью а по пакетам
    data = file.read()
    file.close()
    data_len = len(data)
    print(f'CLIENT: sending file size: {data_len}')
    len_data_in_bytes = data_len.to_bytes(length=8, byteorder='big')
    print(f'CLIENT: sending file size in bytes: {len_data_in_bytes}')
    conn.send(len_data_in_bytes)
    response = conn.recv(package_size).decode()
    print(response)

    for i in range(0, data_len, package_size):
        conn.send(data[i: min(i + package_size, data_len)])
        response = conn.recv(package_size).decode()
        print(response)
        if response != 'ok':
            print('CLIENT: getting file package error')
            print('CLIENT: PROGRAM WAS TERMINATED')
            exit()

    conn.send(f'CLIENT MESSAGE: all file data was sent'.encode())
    response = conn.recv(package_size).decode()
    print(response)

    os.remove(graph_filename)
    print('CLIENT: delivery successfully')
    print('CLIENT: GRAPH DELIVER END\n')


def get_cytoscape_session(conn, cs_session_name=None, package_size=1024):
    if cs_session_name is None:
        cs_session_name = f'client_nx_graph_session_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.cys'
    else:
        cs_session_name += '.cys'

    file = open(cs_session_name, "wb")

    print('\nCLIENT: SESSION RECEIVE START')
    data_len = conn.recv(package_size)
    print(f'CLIENT: sending file size in bytes: {data_len}')
    data_len = int.from_bytes(data_len, byteorder='big')
    print(f'CLIENT: sending file size: {data_len}')
    response = f'CLIENT MESSAGE: received file len: {data_len}'
    conn.send(response.encode())

    received_data_len = 0
    while True:
        try:
            part_data = conn.recv(package_size)
        except BaseException as e:
            print(f'SERVER: GETTING GRAPH: error: {e}')
            exit()

        print(f'in process get {len(part_data)}')
        conn.send('ok'.encode())

        if not part_data:
            break

        file.write(part_data)
        received_data_len += len(part_data)

        if received_data_len == data_len:
            break

    print(f'CLIENT: get bytes: {received_data_len}')
    response = conn.recv(package_size).decode()
    print(response)
    response = f'CLIENT MESSAGE: get bytes: {received_data_len}'.encode()
    conn.send(response)
    print('CLIENT: SESSION RECEIVE END\n')

    file.close()


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


def send_styles(conn, styles_filename, package_size=1024):

    if styles_filename:
        conn.send('TRUE'.encode())
        response = conn.recv(package_size).decode()
        print(response)

        print('\nCLIENT: STYLES DELIVER START')
        file = open(styles_filename, "rb")
        # TODO читать тоже лучше не полностью а по пакетам
        data = file.read()
        file.close()
        data_len = len(data)
        print(f'CLIENT: sending file size: {data_len}')
        len_data_in_bytes = data_len.to_bytes(length=8, byteorder='big')
        print(f'CLIENT: sending file size in bytes: {len_data_in_bytes}')
        conn.send(len_data_in_bytes)
        response = conn.recv(package_size).decode()
        print(response)

        for i in range(0, data_len, package_size):
            conn.send(data[i: min(i + package_size, data_len)])
            response = conn.recv(package_size).decode()
            print(response)
            if response != 'ok':
                print('CLIENT: getting file package error')
                print('CLIENT: PROGRAM WAS TERMINATED')
                exit()

        conn.send(f'CLIENT MESSAGE: all file data was sent'.encode())
        response = conn.recv(package_size).decode()
        print(response)

        # os.remove(styles_filename)
        print('CLIENT: delivery successfully')
        print('CLIENT: STYLES DELIVER END\n')
        return

    conn.send('FALSE'.encode())
    response = conn.recv(package_size).decode()
    print(response)
    return


def client_program(self, cs_session_name=None, layout_algorith='random', styles_filename=None):

    config = configparser.ConfigParser()
    config.read('CytoscapeClient/config_client.ini')
    host = config['REMOTE']['Host']
    port = int(config['REMOTE']['Port'])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    send_styles(client_socket, styles_filename)

    send_nx_graph_to_cytoscape_server(self, client_socket, cs_session_name, layout_algorith)
    get_cytoscape_session(client_socket, cs_session_name)

    client_socket.close()


def init_cytoscape_extension():
    nx.Graph.to_cytoscape_session = client_program
