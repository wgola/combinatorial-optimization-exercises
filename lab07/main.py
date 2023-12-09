from Graph import Graph

if __name__ == "__main__":
    g = Graph()

    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")

    g.add_edge("A", "B", 6)
    g.add_edge("A", "C", 4)
    g.add_edge("A", "D", 8)
    g.add_edge("A", "E", 2)
    g.add_edge("B", "C", 5)
    g.add_edge("B", "D", 8)
    g.add_edge("B", "E", 6)
    g.add_edge("C", "D", 9)
    g.add_edge("C", "E", 3)
    g.add_edge("D", "E", 7)

    Graph.show_graph(g.graph)

    hamilton_cycle, length = g.christofides()

    if hamilton_cycle is None or length is None:
        print("Błąd! Nie można zastosować algorytmu: wagi krawędzi nie spełniają warunku trójkąta lub graf nie jest pełny!")
    else:
        print("Znaleziony cykl hamiltona: ")
        for v in hamilton_cycle:
            print(v + " ->", end=" ")
        print(hamilton_cycle[0])
        print("Długość cyklu: " + str(length))
