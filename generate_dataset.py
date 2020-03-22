from random import randint
from network import Network

network, _ = Network.load("../sample_dataset")
network.save("0-vertices-6,edges-11")
s = 0
t = 5

current_vertices = 6
current_edges = 11
need_vertices = current_vertices
need_edges = current_edges


for m in range(10):
    need_vertices *= 2
    need_edges *= 3

    while current_edges < need_edges:
        for i in range(current_vertices, need_vertices-1):
            if i == current_vertices or randint(0, 2):
                current_edges += 1
                source = i
                destination = randint(0, need_vertices - 2)
                capacity = randint(1, need_vertices - 2)
                if source == s:
                    network.add_edge(source, destination, capacity, source_name="S")
                elif destination == t:
                    network.add_edge(source, destination, capacity, destination_name="T")
                else:
                    network.add_edge(source, destination, capacity)

    network.save(f"{m + 1}-vertices-{network.network_size()},edges-{current_edges}")

