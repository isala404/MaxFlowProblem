from random import randint
from network import Network

vertices = 5
edges = 10

k = 0

while k < 5:
    vertices *= 2
    edges *= 2
    current_edges = 0

    s = randint(0, vertices)
    t = randint(0, vertices)

    while s == t:
        s = randint(0, vertices)
        t = randint(0, vertices)

    network = Network(vertices, s, t)

    while current_edges < edges:
        for i in range(vertices):
            if randint(0, 2):
                current_edges += 1
                source = i
                destination = randint(0, vertices)
                capacity = randint(1, vertices)
                if source == s:
                    network.add_edge(source, destination, capacity, source_name="S")
                elif destination == t:
                    network.add_edge(source, destination, capacity, destination_name="T")
                else:
                    network.add_edge(source, destination, capacity)

                if current_edges >= edges:
                    break
    network.calculate_max_flow()
    if network.max_flow == 0:
        vertices //= 2
        edges //= 2
        continue
    network.save(f"{k + 1}-vertices-{vertices},edges-{edges}")
    k += 1
