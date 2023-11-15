# Zaimplementuj algorytm Bellmana Forda, który dla danego (ustalonego)
# ważonego digrafu (D = (V, A), w) z funkcją wagową w: A → R oraz podanego
# wierzchołka v ∈ V wyznaczy drzewo najkrótszych dróg dla v - długość
# najkrótszej ścieżki z v do wierzchołka oraz którędy biegnie ta droga.
from Graph import Graph

start = "A"

g = Graph(7)
g.add_edge("A", "B", 10)
g.add_edge("A", "D", 10)
g.add_edge("A", "F", 2)
g.add_edge("B", "C", 5)
g.add_edge("C", "D", 4)
g.add_edge("C", "E", -4)
g.add_edge("D", "G", -8)
g.add_edge("D", "B", -9)
g.add_edge("G", "E", 3)
g.add_edge("F", "E", 1)

try:
    paths = g.bellman_ford(start)
    print("Początek startowy: " + start)
    for path in paths.keys():
        print("Długość drogi do wierzhołka " +
              path + ": " + str(paths[path]["length"]), end=". ")
        if len(paths[path]["via"]) != 0:
            print("Wierzchołki pośrednie: " +
                  str(paths[path]["via"]), end=". ")
        print()
except Exception as err:
    print(err)
