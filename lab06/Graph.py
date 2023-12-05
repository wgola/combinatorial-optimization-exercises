import networkx as nx
import igraph as ig
import matplotlib.pyplot as plt

ig.config["plotting.backend"] = "matplotlib"


class Graph():

    def __init__(self):
        self.graph = ig.Graph()

    def add_node(self, name):
        self.graph.add_vertex(name)

    def add_edge(self, a, b, weight):
        self.graph.add_edge(a, b, weight=weight)

    def _is_eulerian(self):
        for degree in [v.degree() for v in self.graph.vs]:
            if degree % 2 != 0:
                return False

        return True

    def _is_semi_eulerian(self):
        odd_degree_verticies = []
        for v in self.graph.vs:
            if v.degree() % 2 != 0:
                odd_degree_verticies.append(v["name"])

        return len(odd_degree_verticies) == 2, odd_degree_verticies

    def _fleury_algorithm(self, start_node):
        graph_copy = self.graph.copy()

        path = [start_node]

        while len(graph_copy.es) != 0:
            edges = [(graph_copy.vs[e.source]["name"],
                      graph_copy.vs[e.target]["name"],
                      e["weight"])
                     for e in [graph_copy.es[i]for i in graph_copy.incident(path[-1])]]

            # Graph.plot(graph_copy)

            if len(edges) == 1:
                source, target, weight = edges[0]
                path.append(target if target != path[-1] else source)

                graph_copy.delete_edges(edges[0])
                graph_copy.delete_vertices(path[-2])
            else:
                for edge in edges:
                    source, target, weight = edge

                    graph_copy.delete_edges(edge)
                    if graph_copy.is_connected():
                        path.append(target if target != path[-1] else source)
                        break
                    else:
                        graph_copy.add_edge(source, target, weight=weight)

        return path

    def plot(graph):
        fig, ax = plt.subplots()

        ig.plot(graph,
                target=ax,
                vertex_label=[v["name"] for v in graph.vs],
                edge_label=[e["weight"] for e in graph.es])
        plt.show()

    def _second_option(self, verticies):
        path = self._fleury_algorithm(verticies[0])

        return_path = [self.graph.vs[v]["name"]
                       for v in self.graph.get_shortest_paths(path[-1], to=path[0], weights="weight")[0]]

        return [*path, *return_path[1:]]

    def _third_option(self, verticies):
        tmp_graph = ig.Graph()
        for v in verticies:
            tmp_graph.add_vertex(v)

        added_edges = []
        for v in verticies:
            for g in verticies:
                if g != v and (v, g) not in added_edges:
                    weight = int(self.graph.distances(
                        source=v, target=g, weights="weight")[0][0])
                    tmp_graph.add_edge(g, v, weight=weight)
                    added_edges.append((g, v))

        g = tmp_graph.to_networkx(
            create_using=nx.Graph,
            vertex_attr_hashable="name")

        min_perfect_matching = nx.min_weight_matching(g, weight="weight")

        graph_copy = self.graph.copy()

        for edge in min_perfect_matching:
            paths = graph_copy.get_shortest_paths(
                edge[0],
                to=edge[1],
                weights="weight")[0]

            for i in range(0, len(paths) - 1):
                eid = graph_copy.get_eid(paths[i], paths[i+1])
                weight = graph_copy.es[eid]["weight"]

                graph_copy.add_edge(paths[i], paths[i+1], weight=weight)

        new_graph = Graph()
        new_graph.graph = graph_copy

        return new_graph._fleury_algorithm(graph_copy.vs[0]["name"])

    def chinese_postman_problem(self):
        if self._is_eulerian():
            start_node = self.graph.vs[0]["name"]
            return self._fleury_algorithm(start_node)

        is_semi_eulerian, verticies = self._is_semi_eulerian()
        if is_semi_eulerian:
            return self._second_option(verticies)

        return self._third_option(verticies)


if __name__ == "__main__":
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")
    g.add_node("G")
    g.add_node("H")
    g.add_node("I")
    g.add_node("J")

    # g.add_edge("A", "B", 3)
    # g.add_edge("A", "F", 4)
    # g.add_edge("B", "F", 8)
    # g.add_edge("B", "C", 5)
    # g.add_edge("C", "F", 14)
    # g.add_edge("C", "E", 10)
    # g.add_edge("C", "D", 5)
    # g.add_edge("D", "E", 9)
    # g.add_edge("E", "F", 6)

    g.add_edge("A", "B", 2)
    g.add_edge("A", "C", 1)
    g.add_edge("B", "F", 2)
    g.add_edge("B", "D", 2)
    g.add_edge("C", "D", 4)
    g.add_edge("D", "E", 2)
    g.add_edge("F", "G", 3)
    g.add_edge("G", "H", 1)
    g.add_edge("E", "H", 4)
    g.add_edge("E", "J", 5)
    g.add_edge("H", "J", 2)
    g.add_edge("H", "I", 2)
    g.add_edge("C", "E", 1)
    g.add_edge("J", "I", 3)
    g.add_edge("D", "G", 3)
    g.add_edge("G", "I", 4)

    Graph.plot(g.graph)

    result = g.chinese_postman_problem()

    print(result)
