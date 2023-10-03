import py4cytoscape as p4c
import networkx as nx
from datetime import datetime


def save_graph_as_cytoscape_file(nx_graph, file_format='gml', file_name=None):
    # if file name wasn't specified, file name created with current datetime info nx_graph_{date and time}
    if file_name is None:
        file_name = f'nx_graph_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'

    # create file in default(gml) or selected format
    match file_format:
        case 'gml':
            nx.write_gml(nx_graph, f'{file_name}.{file_format}')

    # return full file name for import file in cytoscape as network
    return f'{file_name}.{file_format}'


def show_graph_in_cytoscape(nx_graph, file_format='gml', file_name=None):
    # save graph in file with selected format to open in cytoscape
    file_path = save_graph_as_cytoscape_file(nx_graph, file_format, file_name)
    p4c.import_network_from_file(file_path)

    # code for keeping cytoscape opened
    print('Please, input any not empty string to close network:')
    stop_signal = input()

    # destroy current network
    suid = p4c.get_network_suid()
    p4c.delete_network(suid)


# example
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 5)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
show_graph_in_cytoscape(G, file_name='test_graph')
