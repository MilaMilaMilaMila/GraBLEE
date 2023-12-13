import networkx as nx
from CytoscapeClient.cytoscape_client import init_cytoscape_extension

init_cytoscape_extension()

graph = nx.Graph()
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 5)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5)
graph.add_edge(5, 6)
graph.add_edge(6, 7)
graph.add_edge(7, 1)

graph.to_cytoscape_session(cs_session_name='test_session_CIRCULAR_red', layout_algorith='circular', styles_filename='styles_red.xml')





