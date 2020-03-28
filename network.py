# Name - Isala Piyarisi
# IIT - 2018421
# UOW ID - w1742118

import copy
import os
from collections import defaultdict
from typing import NewType
from gui import GUI


class Edge:
    """This class is used to present an Edge or Link in the network"""
    flow = None

    def __init__(self, source: int,
                 destination: int,
                 capacity: int,
                 source_name: str = None,
                 destination_name: str = None):
        """
        Creates a Link between 2 Nodes
        :param source: Index of the source node of the edge
        :param destination: Index of the destination node of the edge
        :param capacity: Maximum flow capacity of the Edge/Link
        :param source_name: Name of source node if Any (ex - S = Source Node of the Network)
                            This is used only when visualizing the graph
        :param destination_name: Name of destination node if Any (ex - T = Sink Node of the Network)
                                 This is used only when visualizing the graph
        """
        self.source = source
        self.destination = destination

        # If the destination_name was not given destination_name is set the index of the source node
        if source_name:
            self.source_name = source_name
        else:
            self.source_name = source

        # If the destination_name was not given destination_name is set the index of the destination node
        if destination_name:
            self.destination_name = destination_name
        else:
            self.destination_name = destination

        self.capacity = capacity

        # flow of edge is 0 at start
        self.flow = 0

        # Placeholder for residual edge
        self.residual_edge = NewType('residual_edge', Edge)

    def is_residual(self) -> bool:
        """
        Check if current node is residual node or not
        :return: current node is residual node or not
        """
        return self.capacity == 0

    def remaining_capacity(self) -> float:
        """
        Get the remaining capacity of the edge
        When there are more and more augmenting paths going though an edge
            - capacity will decrease
            - the flow value will get increased
        :return: remaining capacity
        """
        return self.capacity - self.flow

    def augment(self, bottle_neck):
        """
        Increases the flow on the forward edge by the bottle neck value we found along the augmenting path
        and decreases the flow along the residual edge
        :param bottle_neck:
        """
        self.flow += bottle_neck
        self.residual_edge.flow -= bottle_neck

    def __eq__(self, other):
        """
        Compare two edges are equal or not
        :param other: edge we are comparing with
        :return: whether other edge is equal to current
        """
        return self.source == other.source and self.destination == other.destination and self.capacity == other.capacity

    def __repr__(self):
        return f"Edge {self.source} -> {self.destination} = {self.capacity}"

    def __str__(self):
        return f"{self.source_name} -> {self.destination_name} = {self.capacity}"


class Network:

    def __init__(self, source: int, sink: int, gui: GUI = None):
        self.source = source
        self.sink = sink
        # self.graph = [[]] * graph_size    # If we initialized graph this way element 0 is reference of element 1
        #                                     so if we add something to element 0 it also get added to element 1
        self.graph = defaultdict(list)
        self.visited = defaultdict(bool)
        self.max_flow = 0
        self.gui = gui

    def network_size(self):
        """
        Get the current size of the network
        :rtype: size of the network
        """
        return len(self.graph) + 1

    def add_edge(self,
                 source: int,
                 destination: int,
                 capacity: int = 0,
                 source_name: str = None,
                 destination_name: str = None):
        """
        Connect 2 Nodes in the graph
        :param source: Index of the source node of the edge
        :param destination: Index of the destination node of the edge
        :param capacity: Maximum flow capacity of the Edge/Link
        :param source_name: Name of source node if Any (ex - S = Source Node of the Network)
                            This is used only when visualizing the graph
        :param destination_name: Name of destination node if Any (ex - T = Sink Node of the Network)
                                 This is used only when visualizing the graph
        """
        if capacity < 0:
            raise AttributeError("Edge capacity must be equal grater than 0")

        # Create a object out of Edge class for forward edge
        edge_1 = Edge(source, destination, capacity, source_name, destination_name)
        # Create a object out of Edge class for residual edge
        edge_2 = Edge(destination, source, 0, source_name, destination_name)

        # store a reference to the residual edge
        edge_1.residual_edge = edge_2

        # store a reference to the forward edge in the residual
        edge_2.residual_edge = edge_1

        # residual edges exits to undo bad augmenting paths which do not lead to a maximum flow

        # add the both these edges to the flow graph
        # each edge here is each other's inverse
        # because we want a pointer that we can simply access when we need to access an edge's residual edge
        self.graph[source].append(edge_1)
        self.graph[destination].append(edge_2)

        # If instance of networkX is passed add that created edge to that graph too
        if self.gui:
            self.gui.add_edge(edge_1.source_name, edge_1.destination_name, edge_1)

    def modify_edge(self,
                    source: int,
                    destination: int,
                    capacity: int = 0,
                    source_name: str = None,
                    destination_name: str = None):
        """
        Update the link between 2 Nodes in the graph
        :param source: Index of the source node of the edge
        :param destination: Index of the destination node of the edge
        :param capacity: Maximum flow capacity of the Edge/Link
        :param source_name: Name of source node if Any (ex - S = Source Node of the Network)
                            This is used only when visualizing the graph
        :param destination_name: Name of destination node if Any (ex - T = Sink Node of the Network)
                                 This is used only when visualizing the graph
        """
        for edge in self.graph[source]:
            if edge.source == source and edge.destination == destination_name and not edge.is_residual():
                self.remove_edge(edge.source, edge.destination, edge.capacity)
        self.add_edge(source, destination, capacity, source_name, destination_name)

    def remove_edge(self, source: int, destination: int, capacity: int):
        """
        Remove connection between 2 nodes
        :param source: Index of the source node of the edge
        :param destination: Index of the destination node of the edge
        :param capacity: Maximum flow capacity of the Edge/Link
        """
        # Create a objects out of Edge class
        edge_1 = Edge(source, destination, capacity)
        edge_2 = Edge(destination, source, 0)

        # Keep the copy of the Original edge so it can be passed on the GUI
        original_edge = self.graph[source][self.graph[source].index(edge_1)]

        # Call the remove method of defaultdict which will find and remove edge that match the given edge
        # This method uses __eq__ method defined in the edge class
        self.graph[source].remove(edge_1)
        self.graph[destination].remove(edge_2)

        #
        if self.gui:
            self.gui.G.remove_edge(original_edge.source_name, original_edge.destination_name)

    def calculate_max_flow(self, reset=False, visualize=False):
        """
        Calculate max flow using Ford-Fulkerson Algorithm and Dept First Search
        :param visualize: whether to visualize graph after every new augmenting path was found
        :param reset: reset the graph after max flow calculation
        """
        # if reset is True create copy of graph
        graph = None
        if reset:
            self.visited.clear()
            self.max_flow = 0
            # self.visitedToken = 1
            graph = copy.deepcopy(self.graph)

        # repeatedly calls the depth_first_search till the  and get the bottle neck value found in the augment paths
        # if bottle neck value is zero it means we went all the augmenting paths
        while (f := self._depth_first_search(self.source, float('inf'), visualize)) != 0:
            self.visited.clear()
            # add the bottle neck value to the max flow of the graph
            # because sum of the bottle neck values equals the max flow
            self.max_flow += f

        # restore it after the calculation
        if reset and graph:
            self.graph = graph

    def _depth_first_search(self, node: int, flow: float, visualize=False):
        # if node is the sink node return the augmented path flow
        if node == self.sink:
            return flow

        # Update the node index on the visited array so we can skip that edge if the algorithm try to go though the same
        # edge and cause infinite recursion though stack overflow error
        self.visited[node] = True

        # loop over all the forward and residual edges
        for edge in self.graph[node]:
            # check if we can push at least one flow unit though the edge if not it's point less to go though this edge
            if edge.remaining_capacity() > 0 and not self.visited[edge.destination]:
                # Note - if the graph has very deep augmenting paths this will throw a recursion error it is safety
                # feature added by python to prevent stack overflows

                # Here we calls the depth_first_search recursively by passing the index of destination node of the
                # current edge and new flow value which will be minimum of current flow or remaining capacity of the
                # current edge, Here the flow is trying to capture the bottle neck value so this does keep the bottle
                # neck value or if the current edge's capacity is even smaller make that new flow

                # this process gets repeated until node == self.sink is hit which means we are at the end of the
                # augmenting path and we found the sink node

                # when the sink nodes is reached it will return the bottle neck value of the path taken by the algorithm
                bottle_neck = self._depth_first_search(edge.destination, min(flow, edge.remaining_capacity()))
                # this if condition check the bottle neck is greater than 0
                # if it's not it means we hit dead and and it won't leave sink node and we need to ignore that path
                if bottle_neck > 0:
                    # the we can use the bottle neck value to augment the flow of our augmenting path
                    edge.augment(bottle_neck)

                    # display the current flow the graph
                    if visualize:
                        self.gui.draw(6)
                    return bottle_neck
        return 0

    def save(self, file):
        """
        Write the entire Graph to file which can be read by a human
        :param file: file name
        """
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
        """
        Restore network from text file
        :param file: file name
        :return: Instance of this (Network) class
        """
        gui = GUI()
        with open(f"datasets/{file}", "r") as f:
            lines = f.readlines()

            # Parse meta data of the network
            size = int(lines[0].replace("Size = ", ""))
            s = int(lines[1].replace("Source = ", ""))
            t = int(lines[2].replace("Sink = ", ""))

            # cls is reference to the currant class which is passed by python
            network = cls(s, t, gui)

            for line in lines[3:]:
                # Parse Every Edge of the network from the file
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
