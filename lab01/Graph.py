from abc import ABC


class Graph(ABC):

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
        if self._check_node(node):
            del self.matrix[node]

            for i in range(len(self.matrix)):
                del self.matrix[i][node]

    def add_edge(self, first_node: int, second_node: int):
        pass

    def remove_edge(self, first_node: int, second_node: int):
        pass

    def get_node_degree(self, node: int):
        pass

    def get_graph_degree(self):
        pass

    def get_odd_and_even_nodes_count(self):
        pass

    def get_nodes_degrees(self):
        pass

    def show_graph(self):
        pass

    def _check_node(self, node):
        if node < 0 or node > len(self.matrix):
            raise Exception("Select proper node to create an edge!")

        return True
