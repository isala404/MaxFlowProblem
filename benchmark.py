# Name - Isala Piyarisi
# IIT - 2018421
# UOW ID - w1742118

import math
from tabulate import tabulate
from network import Network
from gui import GUI
import timeit
import os
import matplotlib.pyplot as plt

gui = GUI()

if not os.path.isdir("datasets"):
    raise FileNotFoundError

benchmarks = []

# Iterate though all the files in the datasets folder
for file in sorted(os.listdir("datasets")):
    # Parse file and create a network object out of it
    network, gui = Network.load(file)

    # run the max flow calculation 50 times so minimize the noise in the data
    # calculation may take longer sometimes because CPU was busy doing something else
    time_taken = timeit.timeit(lambda: network.calculate_max_flow(reset=True), number=50) * 1000
    print("Dataset:", file, "Size:", network.network_size(), "MaxFlow:", network.max_flow,
          "Time Taken:", round(time_taken, 2), " milliseconds")

    # Store the data so we can plot a table later
    benchmarks.append({"time_taken": time_taken/2,
                       "dataset_size": network.network_size(),
                       "max_floor": network.max_flow,
                       "edges": int(file.split("edges-")[-1])
                       })

    # If the network is small visualize it
    # I found networkX is having hard time drawing canvas with more than 100 edges
    if network.network_size() < 90:
        gui.draw(network.network_size() // 1.5)

# Plot a Graph that display Time Vs Size
fig, ax = plt.subplots()
ax.plot([i["dataset_size"] for i in benchmarks], [i["time_taken"] for i in benchmarks])
ax.set(ylabel='Time Taken (ms) for 50 iterations', xlabel='Number of Vertices in the graph',
       title='Doubling Hypothesis for MaxFloor Problem')
ax.grid()
plt.show()


# Plot a Table of collected data
print()
table_data = []
for i in range(len(benchmarks)):
    if i == 0:
        table_data.append([benchmarks[i]["dataset_size"],
                           round(benchmarks[i]["time_taken"], 2),
                           "-", "-", benchmarks[i]["max_floor"], benchmarks[i]["edges"],
                           benchmarks[i]["max_floor"] * benchmarks[i]["edges"]])
    else:
        ratio = benchmarks[i]["time_taken"] / benchmarks[i - 1]["time_taken"]
        table_data.append([benchmarks[i]["dataset_size"],
                           round(benchmarks[i]["time_taken"], 2),
                           round(ratio, 2),
                           round(math.log(ratio, 2), 2),
                           benchmarks[i]["max_floor"], benchmarks[i]["edges"],
                           benchmarks[i]["max_floor"] * benchmarks[i]["edges"]
                           ])

print(tabulate(table_data, headers=['N', 'Time', 'Ratio', 'Lg Ratio',
                                    'Max Flow', 'Edges', 'O(Max Flow * Edges)'], tablefmt='orgtbl'))


