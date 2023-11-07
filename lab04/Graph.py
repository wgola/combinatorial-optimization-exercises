from collections import defaultdict
import graphviz


class Graph():

    def __init__(self, verticies):
        self.verticies = verticies
        self.graph = defaultdict(list)

    def add_edge(self, a, b, w):
        self.graph[a].append((b, w))
        self.graph[b].append((a, w))

    def remove_edge(self, a, b):
        self.graph[a] = list(filter(lambda x: x[0] != b, self.graph[a]))
        self.graph[b] = list(filter(lambda x: x[0] != a, self.graph[b]))

        if len(self.graph[a]) == 0:
            del self.graph[a]

        if len(self.graph[b]) == 0:
            del self.graph[b]

    def kruskal_algorithm(self, file_name):
        if len(self.dfs()) != self.verticies:
            print("GRAF NIESPÓJNY")
            return

        tree = Graph(self.verticies)

        edges = []
        for a in self.graph:
            for (b, w) in self.graph[a]:
                if (b, a, w) not in edges:
                    edges.append((a, b, w))

        edges = sorted(edges, key=lambda x: x[2])

        for edge in edges:
            tree.add_edge(edge[0], edge[1], edge[2])
            if tree.has_cycle():
                tree.remove_edge(edge[0], edge[1])

        g = graphviz.Graph()

        for v in range(self.verticies):
            g.node(str(v))

        drawn_edges = []
        sum_of_weights = 0

        for v in self.graph:
            for edge in self.graph[v]:
                if (v, edge[0], edge[1]) not in drawn_edges and (edge[0], v, edge[1]) not in drawn_edges:
                    drawn_edges.append((v, edge[0], edge[1]))
                    if edge in tree.graph[v]:
                        sum_of_weights += edge[1]
                        g.edge(str(v), str(edge[0]),
                               label=str(edge[1]), color="red")
                    else:
                        g.edge(str(v), str(edge[0]), label=str(edge[1]))

        print(sum_of_weights)
        g.view(file_name, cleanup=True, quiet=True, quiet_view=True)

    def has_cycle(self):
        def has_cycle_helper(v, visited, parent):
            visited.append(v)

            for (i, _) in self.graph[v]:
                if i not in visited:
                    if has_cycle_helper(i, visited, v):
                        return True
                elif parent != i:
                    return True

            return False

        visited = []

        for i in range(self.verticies):
            if i not in visited:
                if has_cycle_helper(i, visited, -1):
                    return True

        return False

    def dfs(self):
        def dfs_helper(v, visited):
            visited.append(v)
            for (i, _) in self.graph[v]:
                if i not in visited:
                    dfs_helper(i, visited)

        visited = []

        dfs_helper(0, visited)
        return visited
