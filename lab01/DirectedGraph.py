import networkx as nx
import matplotlib.pyplot as plt


class DirectedGraph():

    def __init__(self):
        self.matrix = []

    def add_node(self):
        if len(self.matrix) == 0:
            self.matrix.append([0])
        else:
            for i in range(len(self.matrix)):
                self.matrix[i].append(0)

            self.matrix.append([0 for _ in range(len(self.matrix[0]))])

    def remove_node(self, node: int):
        if self.__check_node(node):
            del self.matrix[node]

            for i in range(len(self.matrix)):
                del self.matrix[i][node]

    def add_edge(self, first_node: int, second_node: int):
        if self.__check_node(first_node) and self.__check_node(second_node):
            self.matrix[first_node][second_node] = 1

    def remove_edge(self, first_node: int, second_node: int):
        if self.__check_node(first_node) and self.__check_node(second_node):
            self.matrix[first_node][second_node] = 0

    def get_node_degree(self, node: int):
        if self.__check_node(node):
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

    def show_graph(self):
        g = nx.MultiDiGraph()

        for i in range(len(self.matrix)):
            g.add_node(i)

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    g.add_edge(i, j)

        nx.draw(g, with_labels=True)
        plt.show()

    def __check_node(self, node):
        if node < 0 or node > len(self.matrix):
            raise Exception("Select proper node to create an edge!")

        return True
