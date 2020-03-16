from network import Network

n = 12
s = n - 2
t = n - 1

network = Network(n, s, t)


network.add_edge(s, 0, 10)
network.add_edge(s, 1, 5)
network.add_edge(s, 2, 10)

network.add_edge(0, 3, 10)
network.add_edge(1, 2, 10)
network.add_edge(2, 5, 15)
network.add_edge(3, 1, 2)
network.add_edge(3, 6, 15)
network.add_edge(4, 1, 15)
network.add_edge(4, 3, 3)
network.add_edge(5, 4, 4)
network.add_edge(5, 8, 10)
network.add_edge(6, 7, 10)
network.add_edge(7, 4, 10)
network.add_edge(7, 5, 7)

network.add_edge(6, t, 15)
network.add_edge(8, t, 10)

network.calculate_max_flow()

# print(network.network)

print("Maximum Flow is: ", network.max_flow)
for edges in network.graph:
    for edge in edges:
        print(edge.to_string(s, t))
