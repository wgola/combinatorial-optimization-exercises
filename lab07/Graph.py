import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, name):
        self.graph.add_node(name)

    def add_edge(self, start, end, weight):
        self.graph.add_edge(start, end, weight=weight)

    def christofides(self):
        if not self.__check_triangle_inequality():
            return None, None

        if not self.__is_complete_graph():
            return None, None

        minimal_spanning_tree = self.__get_minimal_spanning_tree()

        induced_graph, min_weight_perfect_matching = self.__get_min_matching_and_induced_graph(
            minimal_spanning_tree)

        multigraph = self.__get_multigraph(
            minimal_spanning_tree,
            induced_graph,
            min_weight_perfect_matching)

        eulerian_cycle = self.__get_eulerian_circuit(multigraph)

        hamilton_cycle = self.__get_hamilton_cycle(eulerian_cycle)

        length = self.__show_hamilton_cycle(hamilton_cycle)

        return hamilton_cycle, length

    @staticmethod
    def show_graph(graph, edges_to_color=None):
        pos = nx.shell_layout(graph)

        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos)

        if edges_to_color is not None:
            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=edges_to_color, edge_color="r")

        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edge_labels(
            graph,
            pos,
            nx.get_edge_attributes(graph, "weight"))
        plt.show()

    def __check_triangle_inequality(self):
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                for x in self.graph.nodes:
                    if u != v and v != x and x != u:
                        uv = self.graph.get_edge_data(u, v)["weight"]
                        vx = self.graph.get_edge_data(v, x)["weight"]
                        ux = self.graph.get_edge_data(u, x)["weight"]
                        if uv + vx < ux:
                            return False

        return True

    def __show_hamilton_cycle(self, hamilton_cycle):
        visited_edges = []
        length = 0

        for i in range(0, len(hamilton_cycle) - 1):
            data = self.graph.get_edge_data(
                hamilton_cycle[i],
                hamilton_cycle[i+1])
            length += data["weight"]

            visited_edges.append((hamilton_cycle[i], hamilton_cycle[i+1]))

        data = self.graph.get_edge_data(
            hamilton_cycle[-1],
            hamilton_cycle[0])
        length += data["weight"]

        visited_edges.append((hamilton_cycle[-1], hamilton_cycle[0]))

        self.show_graph(self.graph, visited_edges)

        return length

    def __get_hamilton_cycle(self, eulerian_cycle):
        hamilton_cycle = []
        for (u, v) in eulerian_cycle:
            if u not in hamilton_cycle:
                hamilton_cycle.append(u)
            if v not in hamilton_cycle:
                hamilton_cycle.append(v)
        return hamilton_cycle

    def __get_eulerian_circuit(self, graph):
        eulerian_cycle = nx.eulerian_circuit(graph)

        return eulerian_cycle

    def __get_multigraph(self, minimal_spanning_tree, induced_graph, min_weight_perfect_matching):
        multigraph = nx.MultiGraph(minimal_spanning_tree)

        for (u, v) in min_weight_perfect_matching:
            data = induced_graph.get_edge_data(u, v)
            multigraph.add_edge(u, v, weight=data["weight"])

        return multigraph

    def __get_min_matching_and_induced_graph(self, graph):
        odd_nodes = [v for (v, d) in graph.degree() if d % 2 != 0]

        induced_graph = nx.induced_subgraph(self.graph, odd_nodes)

        min_perfect_matching = nx.min_weight_matching(
            induced_graph, weight="weight")

        return induced_graph, min_perfect_matching

    def __get_minimal_spanning_tree(self):
        minimal_spanning_tree = nx.minimum_spanning_tree(self.graph)
        return minimal_spanning_tree

    def __is_complete_graph(self):
        nodes = self.graph.number_of_nodes()
        edges = self.graph.number_of_edges()
        return nodes * (nodes - 1) / 2 == edges
