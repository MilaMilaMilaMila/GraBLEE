import py4cytoscape as p4c
import networkx as nx
from datetime import datetime
import os
import multiprocessing
import requests.exceptions
import json
import time


def relabel_nodes_to_str(nx_graph):
    mapping = {}
    for node in nx_graph.nodes:
        mapping[node] = str(node)

    return nx.relabel_nodes(nx_graph, mapping)


def save_graph_as_cytoscape_file(nx_graph, file_format='cyjs', file_name=None):
    # if file name wasn't specified, file name created with current datetime info nx_graph_{date and time}
    if file_name is None:
        file_name = f'nx_graph_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'

    # create file in default(gml) or selected format
    full_file_name = f'{file_name}.{file_format}'
    match file_format:
        case 'gml':
            nx.write_gml(nx_graph, full_file_name)
        case 'cyjs':
            str_nodes_nx_graph = relabel_nodes_to_str(nx_graph)
            cyjs_graph_data = nx.cytoscape_data(str_nodes_nx_graph)
            cyjs_file = open(full_file_name, 'w')
            json.dump(cyjs_graph_data, cyjs_file)

    # return full file name for import file in cytoscape as network
    return f'{file_name}.{file_format}'


def save_network_as_session(session_name=None):
    p4c.save_session(filename=session_name)


def run_cytoscape():
    os.system('run_cs_cmd.py')


# function work if cytoscape is opened
def open_network(nx_graph, file_format='gml', file_name=None, save_as_session=False, session_name=None):
    # save graph in file with selected format to open in cytoscape
    file_path = save_graph_as_cytoscape_file(nx_graph, file_format, file_name)
    p4c.import_network_from_file(file_path)

    # code for keeping cytoscape opened
    print('Please, input any not empty string to close network:')
    stop_signal = input()

    # save current network as cytoscape session
    if session_name is None:
        session_name = ''.join(file_path.split('.')[0:-1]) + '_session'

    if save_as_session:
        save_network_as_session(session_name)

    # destroy current network
    suid = p4c.get_network_suid()
    p4c.delete_network(suid)


# function check - is cytoscape opened
# If not - cytoscape will be opened
def show_network_in_cytoscape(nx_graph, file_format='gml', file_name=None, save_as_session=False, session_name=None):
    if __name__ == '__main__':
        try:
            p4c.cytoscape_ping()
        except requests.exceptions.RequestException:
            process1 = multiprocessing.Process(target=run_cytoscape)
            process1.start()

        flag = 1
        while flag:
            try:
                flag = 0
                p4c.cytoscape_ping()
            except requests.exceptions.RequestException:
                flag = 1

        open_network(nx_graph, file_format=file_format, file_name=file_name, save_as_session=save_as_session, session_name=session_name)


# example
graph = nx.Graph()
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 5)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5)

show_network_in_cytoscape(graph, file_format='cyjs', file_name='test_graph', save_as_session=True, session_name="main_test_session")
show_network_in_cytoscape(graph, file_name='test_graph', save_as_session=True)
