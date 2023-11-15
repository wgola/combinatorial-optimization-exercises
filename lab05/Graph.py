from collections import defaultdict
import graphviz
import string
import copy


class Graph():

    def __init__(self, verticies):
        self.verticies = verticies
        self.verticies_list = [i for i in list(
            string.ascii_uppercase)][:self.verticies]
        self.graph = defaultdict(list)

    def add_edge(self, a, b, w):
        self.graph[a].append((b, w))

    def remove_edge(self, a, b):
        self.graph[a] = list(filter(lambda x: x[0] != b, self.graph[a]))

        if len(self.graph[a]) == 0:
            del self.graph[a]

    def bellman_ford(self, start):
        paths = {}

        for v in self.verticies_list:
            paths[v] = {}
            paths[v]["length"] = float("inf")
            paths[v]["via"] = []

        paths[start] = {"length": 0, "via": []}

        self._draw_graph(paths, "before")

        for (v, w) in self.graph[start]:
            paths[v]["length"] = w
            paths[v]["via"] = []

        for _ in range(1, self.verticies - 2):
            for v in [i for i in self.verticies_list if i != start]:
                for u in self.verticies_list:
                    length = float("inf")
                    for (x, w) in self.graph[u]:
                        if x == v:
                            length = w
                            break

                    if paths[v]["length"] > paths[u]["length"] + length:
                        paths[v]["length"] = paths[u]["length"] + length
                        for x in paths[u]["via"]:
                            if x not in paths[v]["via"]:
                                paths[v]["via"].append(x)

                        paths[v]["via"].append(u)

        new_paths = copy.deepcopy(paths)
        for v in [i for i in self.verticies_list if i != start]:
            for u in self.verticies_list:
                length = float("inf")
                for (x, w) in self.graph[u]:
                    if x == v:
                        length = w
                        break

                if new_paths[v]["length"] > new_paths[u]["length"] + length:
                    new_paths[v]["length"] = new_paths[u]["length"] + length
                    for x in new_paths[u]["via"]:
                        if x not in new_paths[v]["via"]:
                            new_paths[v]["via"].append(x)

                    new_paths[v]["via"].append(u)

        for v in self.verticies_list:
            if paths[v]["length"] != new_paths[v]["length"]:
                raise Exception("Błąd - graf zawiera cykle ujemnej długości!")

        self._draw_graph(paths, "after")

        return paths

    def _draw_graph(self, paths, filename):
        g = graphviz.Digraph()
        for v in self.verticies_list:
            g.node(v, label=v + ": " + str(paths[v]["length"]))

        for v in self.verticies_list:
            for (u, w) in self.graph[v]:
                g.edge(v, u, label=str(w))

        g.view(filename, cleanup=True, quiet=True, quiet_view=True)
