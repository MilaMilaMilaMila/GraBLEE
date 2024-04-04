from logging import Logger
import networkx as nx
from datetime import datetime
from client.data_access.file_system import FileSystemRepo
import json
import os
from logging import Logger

class Networkx:
    def __init__(self, l: Logger):
        self.logger = l

    def relabel_nodes_to_str(self, g: nx.Graph):
        self.logger.info('start relabeling graph nodes to str type')

        mapping = {}
        for node in g.nodes:
            mapping[node] = str(node)

        self.logger.info('finish relabeling graph nodes to str type')

        return nx.relabel_nodes(g, mapping)

    def get_layout_pos(self, g: nx.Graph, layout_algo: str):
        self.logger.info('start getting layout nodes positions')

        pos = {}
        match layout_algo:
            case 'spring':
                pos = nx.spring_layout(g)
            case 'shell':
                pos = nx.shell_layout(g)
            case 'circular':
                pos = nx.circular_layout(g)
            case 'random':
                pos = nx.random_layout(g)

        for i in pos:
            pos[i] = (round(pos[i][0], 5), round(pos[i][1], 5))

        self.logger.info('finish getting layout nodes positions')

        return pos

    def set_position_in_cyjs(self, filename, pos):
        self.logger.info('start setting layout nodes positions to cyjs file')

        file = open(filename)
        data = json.load(file)
        file.close()
        os.remove(filename)
        # 100 - affected on distance between nodes
        for i in data["elements"]["nodes"]:
            i['position'] = {"x": pos[int(i['data']['name'])][0] * 100, "y": pos[int(i['data']['name'])][1] * 100}

        file = open(f'{filename}.cyjs', 'w')
        json.dump(data, file)
        file.close()

        self.logger.info('finish setting layout nodes positions to cyjs file')

    def complete_graph_as_cyjs(self, g: nx.Graph, file_format='cyjs', layout_algo='random') -> str:
        self.logger.info('start completing graph as cyjs')

        pos = self.get_layout_pos(g, layout_algo)

        file_name = f'graph_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
        full_file_name = f'{file_name}.{file_format}'

        str_nodes_nx_graph = self.relabel_nodes_to_str(g)
        cyjs_graph_data = nx.cytoscape_data(str_nodes_nx_graph)
        FileSystemRepo.write_cyjs(file_name, cyjs_graph_data)
        self.set_position_in_cyjs(file_name, pos)

        self.logger.info('finish completing graph as cyjs')
        self.logger.info(f'write graph data in {full_file_name}')

        return full_file_name
