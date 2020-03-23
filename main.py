from network import Network
from gui import GUI

gui = GUI()

network = Network(graph_size=6, source=0, sink=0, gui=gui)

network.add_edge(0, 1, 10, source_name="S")
network.add_edge(0, 2, 8, source_name="S")

network.add_edge(1, 2, 5)
network.add_edge(2, 1, 4)

network.add_edge(1, 3, 5)
network.add_edge(2, 4, 10)

network.add_edge(3, 2, 7)
network.add_edge(3, 4, 6)

network.add_edge(4, 3, 10)

network.add_edge(3, 5, 3, destination_name="T")
network.add_edge(4, 5, 14, destination_name="T")

gui.draw(6)
