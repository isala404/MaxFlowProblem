# Name - Isala Piyarisi
# IIT - 2018421
# UOW ID - w1742118

import networkx as nx
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_edge(self, source, destination, edge):
        self.G.add_edge(source, destination, edge=edge)

    def draw(self, vertices):
        edge_data = {}
        max_cap = 0

        # Create the label data for the edges flow/capacity
        for (u, v, d) in self.G.edges(data=True):
            if max_cap < d['edge'].capacity:
                max_cap = d['edge'].capacity
            edge_data[(u, v)] = f"{d['edge'].flow} / {d['edge'].capacity}"

        # Define the size of the canvas
        plt.figure(figsize=(vertices, vertices))

        # Calculate position all the nodes in the canvas
        pos = nx.shell_layout(self.G)

        # Draw edges between nodes
        for (u, v, d) in self.G.edges(data=True):
            nx.draw_networkx_edges(self.G, pos, edgelist=[(u, v)], width=3, alpha=d['edge'].capacity / max_cap,
                                   edge_color='black')

        # Add Labels to the nodes
        nx.draw_networkx_labels(self.G, pos, font_family='sans-serif')

        # Draw the Nodes in the in the canvas
        for node in self.G.nodes():
            if isinstance(node, int):
                nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color="#6b7cff")
            else:
                if node == "S":
                    nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color="#4dbf63")
                else:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color="#ff624a")

        # Draw the label data for the edges
        # label_pos was not documented in the networkX docs I had to go to networkX github page and find it from the
        # source files
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_data, font_color='red', label_pos=0.3)

        plt.axis('off')
        plt.show()
