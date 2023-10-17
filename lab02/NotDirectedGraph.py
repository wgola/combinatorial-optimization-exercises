import numpy as np
import graphviz
from strassen import strassen
from Graph import Graph


class NotDirectedGraph(Graph):

    def __init__(self):
        super().__init__()

    def add_edge(self, first_node: int, second_node: int):
        if self._check_node(first_node) and self._check_node(second_node):
            if first_node == second_node:
                self.matrix[first_node][second_node] += 2
            else:
                self.matrix[first_node][second_node] += 1
                self.matrix[second_node][first_node] += 1

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

    def is_simple_graph(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if (i == j and self.matrix[i][j] != 0) or self.matrix[i][j] > 1:
                    return False

        return True

    def contains_c3_naive(self):
        if not self.is_simple_graph():
            raise Exception("Graph is not simple!")

        if len(self.matrix) < 3:
            return False, None

        for i in range(len(self.matrix)):
            for j in range(i + 1, len(self.matrix)):
                if self.matrix[i][j] == 1:
                    for k in range(j+1, len(self.matrix)):
                        if self.matrix[i][k] == 1 and self.matrix[j][k] == 1:
                            return True, [i, j, k]

        return False, None

    def contains_c3_multiply(self):
        if not self.is_simple_graph():
            raise Exception("Graph is not simple!")

        if len(self.matrix) < 3:
            return False, None

        squared_matrix = strassen(
            np.matrix(self.matrix), np.matrix(self.matrix))

        for i in range(len(self.matrix)):
            for j in range(i + 1, len(self.matrix)):
                if squared_matrix[i, j] > 0 and self.matrix[i][j] == 1:
                    for k in range(j + 1, len(self.matrix)):
                        if self.matrix[i][k] == 1 and self.matrix[k][j]:
                            return True, [i, j, k]
        return False, None

    def show_graph(self):
        graph = graphviz.Graph()

        for i in range(len(self.matrix)):
            graph.node(str(i))

        for i in range(len(self.matrix)):
            for j in range(i, len(self.matrix)):
                if self.matrix[i][j] > 0 and i != j:
                    for _ in range(self.matrix[i][j]):
                        graph.edge(str(i), str(j))
                elif self.matrix[i][j] > 0 and i == j:
                    for _ in range(0, self.matrix[i][j], 2):
                        graph.edge(str(i), str(j))

        graph.view("nieskierowany", cleanup=True, quiet=True, quiet_view=True)
        return "nieskierowany"
