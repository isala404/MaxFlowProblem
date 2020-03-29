from network import Network
import os

file = input("Enter the Filename of the Custom DataSet: ")

if not os.path.exists(file):
    print("File", file, "not found")
    exit(-1)

network, gui = Network.load(os.path.join("../", file))

gui.draw(6)

# Runs the Ford-Fulkerson Algorithm
# If you put visualize as True it will show the graph after it found every augmenting path
network.calculate_max_flow(reset=True, visualize=False)

# Get the MaxFlow of the network
print("MaxFlow of the Network is :", network.max_flow)

# Show updated graph with the final flow values
gui.draw(6)
