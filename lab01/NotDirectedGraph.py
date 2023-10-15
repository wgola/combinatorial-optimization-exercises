import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph


class NotDirectedGraph(Graph):

    def __init__(self):
        super().__init__()

    def add_edge(self, first_node: int, second_node: int):
        if self._check_node(first_node) and self._check_node(second_node):
            if first_node == second_node:
                self.matrix[first_node][second_node] = 2
            else:
                self.matrix[first_node][second_node] = 1
                self.matrix[second_node][first_node] = 1

    def remove_edge(self, first_node: int, second_node: int):
        if self._check_node(first_node) and self._check_node(second_node):
            self.matrix[first_node][second_node] = 0
            self.matrix[second_node][first_node] = 0

    def get_node_degree(self, node: int):
        if self._check_node(node):
            return sum(self.matrix[node])

    def get_graph_degree(self):
        degrees = []
        for i in range(len(self.matrix)):
            degrees.append(self.get_node_degree(i))

        return min(degrees), max(degrees)

    def get_odd_and_even_nodes_count(self):
        degrees = []
        for i in range(len(self.matrix)):
            degrees.append(self.get_node_degree(i))

        odd_nodes_count = len(list(filter(lambda x: x % 2 != 0, degrees)))
        even_nodes_count = len(list(filter(lambda x: x % 2 == 0, degrees)))

        return odd_nodes_count, even_nodes_count

    def get_nodes_degrees(self):
        degrees = []
        for i in range(len(self.matrix)):
            degrees.append(self.get_node_degree(i))

        degrees.sort(reverse=True)

        return degrees

    def show_graph(self):
        g = nx.MultiGraph()

        for i in range(len(self.matrix)):
            g.add_node(i)

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1 or self.matrix[i][j] == 2:
                    g.add_edge(i, j)

        nx.draw(g, with_labels=True)
        plt.show()
