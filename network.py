from typing import NewType
from queue import Queue


class Edge:
    flow = None

    def __init__(self, source: int, destination: int, capacity: float):
        self.source = source
        self.destination = destination
        self.capacity = capacity
        self.flow = 0
        self.residual_node = NewType('residual_node', Edge)

    def is_residual(self) -> bool:
        return self.capacity == 0

    def remaining_capacity(self) -> float:
        return self.capacity - self.flow

    def augment(self, bottle_neck):
        self.flow += bottle_neck
        self.residual_node.flow -= bottle_neck


class Network:

    def __int__(self, network_size: int, source: int, sink: int):
        self.source = source
        self.sink = sink
        self.network = [[]] * network_size
        self.network_size = network_size
        self.visited = [False] * self.network_size
        self.max_flow = 0

    def add_edge(self, node_1: int, node_2: int, capacity: float):
        if capacity <= 0:
            raise AttributeError("Edge capacity must be grater than 0")
        if node_1 > self.network_size or node_1 > self.network_size:
            raise AttributeError(f"Network should not have nodes more than {self.network_size}")

        edge_1 = Edge(node_1, node_2, capacity)
        edge_2 = Edge(node_2, node_1, 0)
        edge_1.residual_node = edge_2
        edge_2.residual_node = edge_1
        self.network[node_1].append(edge_1)
        self.network[node_2].append(edge_2)

    def calculate_max_flow(self):
        while (f := self.depth_first_search(self.source, float('inf'))) != 0:
            self.max_flow += f

    # def breath_first_search(self, source: int, sink: int, ):
    #     visited = [False] * self.network_size
    #     search_queue = Queue(maxsize=self.network_size)
    #     search_queue.put(source)
    #     visited[source] = True
    #     while not search_queue.empty():
    #         source_vertex = search_queue.get()
    #
    #         for i, adjacent_vertex in enumerate(self.network[source_vertex]):
    #             if not visited[i]

    def depth_first_search(self, node: int, flow: float):
        if node == self.sink:
            return flow

        self.visited[node] = True

        for edge in self.network[node]:
            if edge.remaining_capacity() > 0 and self.visited[edge.destination]:
                bottle_neck = self.depth_first_search(edge.destination, min(flow, edge.remaining_capacity()))

                if bottle_neck > 0:
                    edge.augment(bottle_neck)
                    return bottle_neck
        return 0
