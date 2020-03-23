import copy
import os
from collections import defaultdict
from typing import NewType
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

    def __str__(self):
        return f"{self.source_name} -> {self.destination_name} = {self.capacity}"


class Network:

    def __init__(self, graph_size: int, source: int, sink: int, gui: GUI = None):
        self.source = source
        self.sink = sink
        # self.graph = [[]] * graph_size    # If we initialized graph this way element 0 is reference of element 1
        #                                     so if we add something to element 0 it also get added to element 1
        self.graph = defaultdict(list)
        self.visited = [-1] * graph_size
        self.visitedToken = 1
        self.max_flow = 0
        self.gui = gui

    def network_size(self):
        return len(self.graph) + 1

    def add_edge(self,
                 source: int,
                 destination: int,
                 capacity: float,
                 source_name: str = None,
                 destination_name: str = None):

        if capacity <= 0:
            raise AttributeError("Edge capacity must be grater than 0")
        if source > self.network_size() or source > self.network_size():
            raise AttributeError(f"Network should not have nodes more than {self.network_size()}")

        edge_1 = Edge(source, destination, capacity, source_name, destination_name)
        edge_2 = Edge(destination, source, 0, source_name, destination_name)
        edge_1.residual_node = edge_2
        edge_2.residual_node = edge_1
        self.graph[source].append(edge_1)
        self.graph[destination].append(edge_2)

        if self.gui:
            self.gui.add_edge(edge_1.source_name, edge_1.destination_name, edge_1.capacity)

    def calculate_max_flow(self, reset=True):
        graph = None
        if reset:
            self.visited = [-1] * self.network_size()
            self.max_flow = 0
            self.visitedToken = 1
            graph = copy.deepcopy(self.graph)
        while (f := self._depth_first_search(self.source, float('inf'))) != 0:
            self.visitedToken += 1
            self.max_flow += f

        if reset and graph:
            self.graph = graph

    def _depth_first_search(self, node: int, flow: float):
        if node == self.sink:
            return flow

        self.visited[node] = self.visitedToken

        for edge in self.graph[node]:
            if edge.remaining_capacity() > 0 and self.visited[edge.destination] != self.visitedToken:
                bottle_neck = self._depth_first_search(edge.destination, min(flow, edge.remaining_capacity()))
                if bottle_neck > 0:
                    edge.augment(bottle_neck)
                    return bottle_neck
        return 0

    def save(self, file):
        if not os.path.isdir("datasets"):
            os.mkdir("datasets")

        with open(f"datasets/{file}", "w") as f:
            f.write(f"Size = {self.network_size()}\n")
            f.write(f"Source = {self.source}\n")
            f.write(f"Sink = {self.sink}\n")
            for node in sorted(self.graph):
                for edge in self.graph[node]:
                    if edge.capacity > 0:
                        f.write(f"{edge}\n")

    @classmethod
    def load(cls, file):
        gui = GUI()
        with open(f"datasets/{file}", "r") as f:
            lines = f.readlines()
            size = int(lines[0].replace("Size = ", ""))
            s = int(lines[1].replace("Source = ", ""))
            t = int(lines[2].replace("Sink = ", ""))

            network = cls(size, s, t, gui)

            for line in lines[3:]:
                line = line.replace("S", str(s))
                line = line.replace("T", str(t))
                line = line.replace(" -> ", ",")
                line = line.replace(" = ", ",")
                line = line.strip()
                source, destination, capacity = map(int, line.split(","))
                if source == s:
                    network.add_edge(source, destination, capacity, source_name="S")
                elif destination == t:
                    network.add_edge(source, destination, capacity, destination_name="T")
                else:
                    network.add_edge(source, destination, capacity)
        return network, gui
