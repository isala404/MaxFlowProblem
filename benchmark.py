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
    time_taken = timeit.timeit(lambda: network.calculate_max_flow(reset=True), number=50) * 1000
    print("Dataset:", file, "Size:", network.network_size(), "MaxFlow:", network.max_flow,
          "Time Taken:", round(time_taken, 2), " milliseconds")
    time_array.append(round(time_taken, 2))
    dataset_size.append(network.network_size())
    if network.network_size() < 90:
        gui.draw(network.network_size() // 1.5)

fig, ax = plt.subplots()
ax.plot(time_array, dataset_size)

ax.set(xlabel='Time Taken (ms) for 50 iterations', ylabel='Number of Vertices in the graph',
       title='Doubling Hypothesis for MaxFloor Problem')
ax.grid()
plt.show()
