from network import Network
from gui import GUI


n = 12
s = n - 2
t = n - 1

gui = GUI()


network = Network(6, 0, 5, gui)

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


network.calculate_max_flow()

gui.draw()

print("Maximum Flow is: ", network.max_flow)