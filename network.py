from typing import NewType
from queue import Queue
from gui import GUI


class Edge:
    flow = None

    def __init__(self, source: int,
                 destination: int,
                 capacity: float,
                 source_name: str = None,
                 destination_name: str = None):

        self.source = source
        self.destination = destination

        if source_name:
            self.source_name = source_name
        else:
            self.source_name = source

        if destination_name:
            self.destination_name = destination_name
        else:
            self.destination_name = destination

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

    def __repr__(self):
        return f"Edge {self.source} -> {self.destination}"


class Network:

    def __init__(self, graph_size: int, source: int, sink: int, gui: GUI):
        self.source = source
        self.sink = sink
        # self.graph = [[]] * graph_size    # If we initialized graph this way element 0 is reference of element 1
        #                                     so if we add something to element 0 it also get added to element 1
        self.graph = [[] for i in range(graph_size)]
        self.graph_size = graph_size
        self.visited = [-1] * self.graph_size
        self.max_flow = 0
        self.visitedToken = 1
        self.gui = gui

    def add_edge(self,
                 source: int,
                 destination: int,
                 capacity: float,
                 source_name: str = None,
                 destination_name: str = None):

        if capacity <= 0:
            raise AttributeError("Edge capacity must be grater than 0")
        if source > self.graph_size or source > self.graph_size:
            raise AttributeError(f"Network should not have nodes more than {self.graph_size}")

        edge_1 = Edge(source, destination, capacity, source_name, destination_name)
        edge_2 = Edge(destination, source, 0, source_name, destination_name)
        edge_1.residual_node = edge_2
        edge_2.residual_node = edge_1
        self.graph[source].append(edge_1)
        self.graph[destination].append(edge_2)

        self.gui.add_edge(edge_1.source_name, edge_1.destination_name, edge_1.capacity)

    def calculate_max_flow(self):
        while (f := self.depth_first_search(self.source, float('inf'))) != 0:
            self.visitedToken += 1
            self.max_flow += f

    def depth_first_search(self, node: int, flow: float):
        if node == self.sink:
            return flow

        self.visited[node] = self.visitedToken

        for edge in self.graph[node]:
            if edge.remaining_capacity() > 0 and self.visited[edge.destination] != self.visitedToken:
                bottle_neck = self.depth_first_search(edge.destination, min(flow, edge.remaining_capacity()))
                if bottle_neck > 0:
                    edge.augment(bottle_neck)
                    return bottle_neck
        return 0
