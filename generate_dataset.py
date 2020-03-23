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


for m in range(9):
    need_vertices *= 2
    need_edges *= 2
    first_iteration = True
    while current_edges < need_edges:
        if first_iteration:
            for i in range(current_vertices, need_vertices - 1):
                current_edges += 1
                add_edge(i, need_vertices)
            current_vertices = need_vertices
            first_iteration = False
        else:
            for i in range(0, need_vertices - 1):
                if randint(0, 2):
                    if current_edges >= need_edges:
                        break
                    current_edges += 1
                    add_edge(i, need_vertices)

    network.save(f"{m + 1}-vertices-{network.network_size()},edges-{current_edges}")
