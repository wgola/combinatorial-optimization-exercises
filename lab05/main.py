# Zaimplementuj algorytm Bellmana Forda, który dla danego (ustalonego)
# ważonego digrafu (D = (V, A), w) z funkcją wagową w: A → R oraz podanego
# wierzchołka v ∈ V wyznaczy drzewo najkrótszych dróg dla v - długość
# najkrótszej ścieżki z v do wierzchołka oraz którędy biegnie ta droga.
from Graph import Graph

start = "A"

g = Graph(6)
g.add_edge("A", "B", 8)
g.add_edge("A", "D", 6)
g.add_edge("B", "C", -1)
g.add_edge("D", "B", 3)
g.add_edge("D", "E", -2)
g.add_edge("C", "D", -2)
g.add_edge("C", "F", 3)
g.add_edge("E", "F", 2)
paths = g.bellman_ford(start)

print("Początek startowy: " + start)
for path in paths.keys():
    print("Długość drogi do wierzhołka " +
          path + ": " + str(paths[path]["length"]), end=". ")
    if len(paths[path]["via"]) != 0:
        print("Wierzchołki pośrednie: " + str(paths[path]["via"]), end=". ")
    print()
