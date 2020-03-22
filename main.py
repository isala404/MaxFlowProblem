from network import Network
from gui import GUI
import timeit
import os
import matplotlib.pyplot as plt
gui = GUI()

if not os.path.isdir("datasets"):
    raise FileNotFoundError

dataset_size = []
time_array = []

for file in sorted(os.listdir("datasets")):
    network, gui = Network.load(file)
    time_taken = timeit.timeit(lambda: network.calculate_max_flow(), number=10000) * 1000
    print("Dataset:", file, "Size:", network.network_size(), "MaxFlow:", network.max_flow,
          "Time Taken:", round(time_taken, 2), " milliseconds")
    time_array.append(round(time_taken, 2))
    dataset_size.append(network.network_size())
    if network.network_size() < 90:
        gui.draw(network.network_size() // 1.5)

fig, ax = plt.subplots()
ax.plot(time_array, dataset_size)

ax.set(xlabel='Time Taken (ms) for 10000 iterations', ylabel='Number of Vertices in the graph',
       title='Doubling Hypothesis for MaxFloor Problem')
ax.grid()
plt.show()

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
