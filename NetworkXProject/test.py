import networkx as nx
from CytoscapeClient.cytoscape_client import init_cytoscape_extension
import matplotlib.pyplot as plt

init_cytoscape_extension()

graph = nx.Graph()
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 5)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5)
nx.write_gml(graph, "no_pos.gml")
# nx.draw(graph)
# plt.show()
graph.add_node(8, pos=(0.345, 2.56))
nx.write_gml(graph, "no_lay.gml")
# nx.draw(graph)
# plt.show()
# pos = nx.circular_layout(graph)
# nx.draw(graph, pos)
# plt.show()
# nx.set_node_attributes(graph, pos, 'pos')
# print(pos)
# for i in pos:
#     pos[i] = (pos[i][0], pos[i][1])
    # print(i, pos[i][0], pos[i][1])
    # new_pos = (round(pos[i][0], 4), round(pos[i][1], 4))
    # pos[i] = new_pos
    # print(str(new_pos))

# print(pos)
# nx.set_node_attributes(graph, pos, 'pos')
# nx.write_gml(graph, "lay.gml")
graph.to_cytoscape_session(cs_session_name='test_session', layout_algorith='circular')
# graph.to_cytoscape_session()



# G = nx.Graph()
# G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])
# nx.draw(G)
# plt.show()
# # Задание координат вершин
# pos = {1: (0, 0), 2: (1, 1), 3: (2, 0), 4: (3, 1), 5: (4, 0)}
#
# # Установка координат вершин в графе G
# nx.set_node_attributes(G, pos, 'pos')
#
# # Визуализация графа с заданными координатами вершин
# nx.draw(G)
# plt.show()
#
# # pos = nx.circular_layout(G)
#
# print(pos)


