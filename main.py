# Name - Isala Piyarisi
# IIT - 2018421
# UOW ID - w1742118

from network import Network
from gui import GUI
import sys
if sys.version_info[0] < 3 and sys.version_info[1] <= 8:
    raise Exception("To run this program you need Python 3.8 or higher")

# Setup the GUI
gui = GUI()

# Setup the Graph
network = Network(source=0, sink=5, gui=gui)

# Added edge
# Here the first parameter is the source of the Edge
# second parameter is the destination of the Edge
# third parameter is the capacity of the Edge
# if this edge's source is the source of the network put source_name="S"
# if this edge's destination is the sink of the network put destination_name="T"
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

# Displays the Graph Before running the Ford-Fulkerson Algorithm on it
gui.draw(6)

# Runs the Ford-Fulkerson Algorithm
# If you put visualize as True it will show the graph after it found every augmenting path
network.calculate_max_flow(reset=True, visualize=False)

# Get the MaxFlow of the network
print("MaxFlow of the Network is :", network.max_flow)

# Show updated graph with the final flow values
gui.draw(6)

# Update the capacity of edges goes from 3 - 2
network.modify_edge(3, 2, 5)
# Show the new graph
gui.draw(6)

# Remove the edge from 4 - 5
network.remove_edge(4, 5, 14)
# Show the new graph
gui.draw(6)

# Runs the Ford-Fulkerson Algorithm on the new graph
network.calculate_max_flow(reset=True, visualize=False)
# Print the Max flow of the new graph
print("MaxFlow of the Network is :", network.max_flow)
