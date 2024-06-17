import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

import networkx as nx
from client.main import init_cytoscape_extension

# add cytoscape extension to networkx.Graph
init_cytoscape_extension()

graph = nx.Graph()

graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 5)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5)
graph.add_edge(5, 6)

# с помощью этой части кода я создвала большие графы
# for i in range(6, 100000):
#     graph.add_edge(i, i + 1)

# get cytoscape session file in the current file directory
graph.to_cytoscape_session(cs_session_name='session',
                           layout_algo='circular',
                           styles_filename='styles_red.xml'
                           )
