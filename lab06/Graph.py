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

    def chinese_postman_problem(self):
        if self._is_eulerian():
            start_node = self.graph.vs[0]["name"]
            return self._fleury_algorithm(start_node)

        is_semi_eulerian, verticies = self._is_semi_eulerian()
        if is_semi_eulerian:
            return self._second_case(verticies)

        return self._third_case(verticies)

    def plot(graph):
        _, ax = plt.subplots()

        ig.plot(graph,
                layout="fr",
                target=ax,
                vertex_label=[v["name"] for v in graph.vs],
                edge_label=[e["weight"] for e in graph.es],
                align_label=True)
        plt.show()

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

    def _second_case(self, verticies):
        path = self._fleury_algorithm(verticies[0])

        return_path = [self.graph.vs[v]["name"]
                       for v in self.graph.get_shortest_paths(path[-1], to=path[0], weights="weight")[0]]

        return [*path, *return_path[1:]]

    def _third_case(self, verticies):
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

        new_graph = Graph()
        new_graph.graph = self.graph.copy()

        for edge in min_perfect_matching:
            paths = new_graph.graph.get_shortest_paths(
                edge[0],
                to=edge[1],
                weights="weight")[0]

            for i in range(0, len(paths) - 1):
                eid = new_graph.graph.get_eid(paths[i], paths[i+1])
                weight = new_graph.graph.es[eid]["weight"]

                new_graph.graph.add_edge(paths[i], paths[i+1], weight=weight)

        return new_graph._fleury_algorithm(new_graph.graph.vs[0]["name"])
