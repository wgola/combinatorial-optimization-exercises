import numpy as np
import graphviz
from strassen import strassen
from Graph import Graph


class DirectedGraph(Graph):

    def __init__(self):
        super().__init__()

    def add_edge(self, first_node: int, second_node: int):
        if self._check_node(first_node) and self._check_node(second_node):
            self.matrix[first_node][second_node] += 1

    def remove_edge(self, first_node: int, second_node: int):
        if self._check_node(first_node) and self._check_node(second_node):
            self.matrix[first_node][second_node] = 0

    def get_node_degree(self, node: int):
        if self._check_node(node):
            out_degree = sum(self.matrix[node])
            in_degree = 0
            for i in range(len(self.matrix)):
                in_degree += self.matrix[i][node]

            return out_degree, in_degree

    def get_graph_degree(self):
        degrees = []
        for i in range(len(self.matrix)):
            out_degree, in_degree = self.get_node_degree(i)
            degrees.append(out_degree + in_degree)

        return min(degrees), max(degrees)

    def get_odd_and_even_nodes_count(self):
        degrees = []
        for i in range(len(self.matrix)):
            out_degree, in_degree = self.get_node_degree(i)
            degrees.append(out_degree + in_degree)

        odd_nodes_count = len(list(filter(lambda x: x % 2 != 0, degrees)))
        even_nodes_count = len(list(filter(lambda x: x % 2 == 0, degrees)))

        return odd_nodes_count, even_nodes_count

    def get_nodes_degrees(self):
        degrees = []
        for i in range(len(self.matrix)):
            out_degree, in_degree = self.get_node_degree(i)
            degrees.append(out_degree + in_degree)

        degrees.sort(reverse=True)

        return degrees

    def is_simple_graph(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if (i == j and self.matrix[i][j] != 0) or self.matrix[i][j] > 1 or (self.matrix[i][j] == 1 and self.matrix[j][i] == 1):
                    return False

        return True

    def contains_c3_naive(self):
        if not self.is_simple_graph():
            raise Exception("Graph is not simple!")

        if len(self.matrix) < 3:
            return False, None

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 1:
                    for k in range(len(self.matrix)):
                        if self.matrix[j][k] == 1 and self.matrix[k][i] == 1:
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
            for j in range(len(self.matrix)):
                if squared_matrix[i, j] > 0 and self.matrix[j][i] == 1:
                    for k in range(len(self.matrix)):
                        if self.matrix[i][k] == 1 and self.matrix[k][j]:
                            return True, [i, k, j]
        return False, None

    def show_graph(self):
        graph = graphviz.Digraph()

        for i in range(len(self.matrix)):
            graph.node(str(i))

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] > 0:
                    for _ in range(self.matrix[i][j]):
                        graph.edge(str(i), str(j))

        graph.view("skierowany", cleanup=True, quiet=True, quiet_view=True)
        return "skierowany"
