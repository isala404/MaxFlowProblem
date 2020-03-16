from network import Network
from gui import GUI


n = 12
s = n - 2
t = n - 1

gui = GUI()

network = Network(n, s, t, gui)


# network.add_edge(s, 0, 10, source_name="S")
# network.add_edge(s, 1, 5, source_name="S")
# network.add_edge(s, 2, 10, source_name="S")
#
# network.add_edge(0, 3, 10)
# network.add_edge(1, 2, 10)
# network.add_edge(2, 5, 15)
# network.add_edge(3, 1, 2)
# network.add_edge(3, 6, 15)
# network.add_edge(4, 1, 15)
# network.add_edge(4, 3, 3)
# network.add_edge(5, 4, 4)
# network.add_edge(5, 8, 10)
# network.add_edge(6, 7, 10)
# network.add_edge(7, 4, 10)
# network.add_edge(7, 5, 7)
#
# network.add_edge(6, t, 15, destination_name="T")
# network.add_edge(8, t, 10, destination_name="T")


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
# print(network.network)

print("Maximum Flow is: ", network.max_flow)
# for edges in network.graph:
#     for edge in edges:
#         print(edge.to_string(s, t))
