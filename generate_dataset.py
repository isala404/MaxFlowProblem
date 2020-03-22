from random import randint
from network import Network

network, _ = Network.load("../sample_dataset")
network.save("0-vertices-5,edges-10")
s = 0
t = 5

current_vertices = 5
current_edges = 10
need_vertices = 5
need_edges = 10

k = 0

for _ in range(5):
    need_vertices *= 2
    need_edges *= 2

    while current_edges < need_edges:
        for i in range(current_vertices, need_edges):
            if i == current_vertices or randint(0, 2):
                current_edges += 1
                source = i
                destination = randint(0, need_vertices)
                capacity = randint(1, need_vertices)
                if source == s:
                    network.add_edge(source, destination, capacity, source_name="S")
                elif destination == t:
                    network.add_edge(source, destination, capacity, destination_name="T")
                else:
                    network.add_edge(source, destination, capacity)

                if current_edges >= need_edges:
                    break
            current_vertices += 1

    network.save(f"{k + 1}-vertices-{current_vertices},edges-{current_edges}")


