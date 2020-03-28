# Name - Isala Piyarisi
# IIT - 2018421
# UOW ID - w1742118

from network import Network
from gui import GUI
import sys
if sys.version_info[0] < 3 and sys.version_info[1] <= 8:
    raise Exception("To run this program you need Python 3.8 or higher")

gui = GUI()

network = Network(source=0, sink=5, gui=gui)

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

network.calculate_max_flow(reset=True)

print("Max Floor", network.max_flow)

gui.draw(6)

network.modify_edge(3, 2, 5)
gui.draw(6)
network.remove_edge(4, 5, 14)
gui.draw(6)

network.calculate_max_flow(reset=True)
print("Max Floor", network.max_flow)
