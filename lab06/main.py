import sys
from Graph import Graph


def first_case(graph):
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("E")
    graph.add_node("F")

    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "F", 1)
    graph.add_edge("A", "D", 1)
    graph.add_edge("A", "E", 1)
    graph.add_edge("B", "C", 1)
    graph.add_edge("B", "D", 1)
    graph.add_edge("B", "E", 1)
    graph.add_edge("C", "D", 1)
    graph.add_edge("D", "E", 1)
    graph.add_edge("E", "F", 1)


def second_case(graph):
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("E")
    graph.add_node("F")

    graph.add_edge("A", "B", 3)
    graph.add_edge("A", "F", 4)
    graph.add_edge("B", "F", 8)
    graph.add_edge("B", "C", 5)
    graph.add_edge("C", "F", 14)
    graph.add_edge("C", "E", 10)
    graph.add_edge("C", "D", 5)
    graph.add_edge("D", "E", 9)
    graph.add_edge("E", "F", 6)


def third_case(graph):
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("E")
    graph.add_node("F")
    graph.add_node("G")
    graph.add_node("H")
    graph.add_node("I")
    graph.add_node("J")

    graph.add_edge("A", "B", 2)
    graph.add_edge("A", "C", 1)
    graph.add_edge("B", "F", 2)
    graph.add_edge("B", "D", 2)
    graph.add_edge("C", "D", 4)
    graph.add_edge("D", "E", 2)
    graph.add_edge("F", "G", 3)
    graph.add_edge("G", "H", 1)
    graph.add_edge("E", "H", 4)
    graph.add_edge("E", "J", 5)
    graph.add_edge("H", "J", 2)
    graph.add_edge("H", "I", 2)
    graph.add_edge("C", "E", 1)
    graph.add_edge("J", "I", 3)
    graph.add_edge("D", "G", 3)
    graph.add_edge("G", "I", 4)


if __name__ == "__main__":
    version = sys.argv[1]
    g = Graph()

    match version:
        case "1": first_case(g)
        case "2": second_case(g)
        case "3": third_case(g)

    path = g.chinese_postman_problem()

    print("Znaleziona trasa: ")
    for v in path[:-1]:
        print(v + " ->", end=" ")
    print(path[-1])

    Graph.plot(g.graph)
