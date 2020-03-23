import networkx as nx
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_edge(self, source, destination, weight):
        self.G.add_edge(source, destination, weight=weight)

    def draw(self, vertices):
        edge_data = {}
        for (u, v, d) in self.G.edges(data=True):
            edge_data[(u, v)] = d['weight']

        plt.figure(figsize=(vertices, vertices))

        pos = nx.shell_layout(self.G)

        for (u, v, d) in self.G.edges(data=True):
            nx.draw_networkx_edges(self.G,
                                   pos,
                                   edgelist=[(u, v)],
                                   width=3,
                                   alpha=d['weight'] / max(edge_data.values()),
                                   edge_color='black')

        nx.draw_networkx_labels(self.G, pos, font_family='sans-serif')

        for node in self.G.nodes():
            if isinstance(node, int):
                nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color="#6b7cff")
            else:
                if node == "S":
                    nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color="#4dbf63")
                else:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color="#ff624a")

        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_data, font_color='red')

        plt.axis('off')
        plt.show()
