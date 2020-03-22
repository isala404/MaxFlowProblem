from network import Network
from gui import GUI
import timeit
import os

gui = GUI()

if not os.path.isdir("datasets"):
    raise FileNotFoundError

for file in sorted(os.listdir("datasets")):
    network, gui = Network.load(file)
    time_taken = timeit.timeit(lambda: network.calculate_max_flow(), number=1000) * 1000
    print("Dataset:", file, "Size:", network.network_size(), "MaxFlow:", network.max_flow,
          "Time Taken:", round(time_taken, 2), " milliseconds")
    # gui.draw(network.graph_size // 1.5)

# network = Network(6, 0, 5, gui)
#
# network.add_edge(0, 1, 10, source_name="S")
# network.add_edge(0, 2, 8, source_name="S")
#
# network.add_edge(1, 2, 5)
# network.add_edge(2, 1, 4)
#
# network.add_edge(1, 3, 5)
# network.add_edge(2, 4, 10)
#
# network.add_edge(3, 2, 7)
# network.add_edge(3, 4, 6)
#
# network.add_edge(4, 3, 10)
#
# network.add_edge(3, 5, 3, destination_name="T")
# network.add_edge(4, 5, 14, destination_name="T")

# network.save("sample")
