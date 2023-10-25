import graphviz


class NotDirectedGraph():

    def __init__(self):
        self.matrix = []

    def add_node(self):
        if len(self.matrix) == 0:
            self.matrix.append([None])
        else:
            for i in range(len(self.matrix)):
                self.matrix[i].append(None)

            self.matrix.append([None for _ in range(len(self.matrix[0]))])

    def add_edge(self, first_node: int, second_node: int, weight: int):
        if self._check_node(first_node) and self._check_node(second_node):
            self.matrix[first_node][second_node] = 0
            self.matrix[second_node][first_node] = 0
            if first_node == second_node:
                self.matrix[first_node][second_node] += weight
            else:
                self.matrix[first_node][second_node] += weight
                self.matrix[second_node][first_node] += weight

    def show_graph(self, file_name):
        graph = graphviz.Graph()

        for i in range(len(self.matrix)):
            graph.node(str(i))

        for i in range(len(self.matrix)):
            for j in range(i, len(self.matrix)):
                if self.matrix[i][j] is not None:
                    graph.edge(str(i), str(j), label=str(self.matrix[i][j]))

        graph.view(file_name, cleanup=True, quiet=True, quiet_view=True)

    def _check_node(self, node):
        if node < 0 or node > len(self.matrix):
            raise Exception("Select proper node to create an edge!")

        return True
