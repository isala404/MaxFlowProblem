# Name - Isala Piyarisi
# IIT - 2018421
# UOW ID - w1742118

# This is simple script I wrote to scale a given graph n times by 2 in every iteration

from random import randint
from network import Network
import os

# Run this if you want to override the current dataset

if not os.path.isdir("datasets"):
    os.makedirs("datasets")

network, _ = Network.load("../sample_dataset")
network.save("0-vertices-6,edges-11")
s = 0
t = 5

current_vertices = 6
current_edges = 11
need_vertices = current_vertices
need_edges = current_edges


def add_edge(source_node, network_size):
    if source_node == t:
        return False
    destination = randint(0, need_vertices - 2)
    while destination == s:
        destination = randint(0, need_vertices - 2)

    capacity = randint(1, network_size)
    if source_node == s:
        network.add_edge(source_node, destination, capacity, source_name="S")
    elif destination == t:
        network.add_edge(source_node, destination, capacity, destination_name="T")
    else:
        network.add_edge(source_node, destination, capacity)
    return True


for m in range(8):
    need_vertices *= 2
    need_edges *= 2
    first_iteration = True

    for i in range(current_vertices, need_vertices - 1):
        if add_edge(i, need_vertices - 1):
            current_edges += 1
    current_vertices = need_vertices

    while current_edges < need_edges:
        for i in range(0, need_vertices - 1):
            if randint(0, 2):
                if current_edges >= need_edges:
                    break
                if add_edge(i, need_vertices - 1):
                    current_edges += 1

    network.save(f"{m + 1}-vertices-{network.network_size()},edges-{current_edges}")
