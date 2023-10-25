from NotDirectedGraph import NotDirectedGraph


def main():
    tests = int(input())

    for _ in range(tests):
        graph = NotDirectedGraph()

        first_line = input()
        nodes_count = int(first_line[2])

        for _ in range(nodes_count):
            graph.add_node()

        second_line = input()
        edges = second_line.split(" ")
        for edge in edges:
            start, end, weight = parse_edge(edge)
            graph.add_edge(start, end, weight)

        graph.show_graph("abc")


def parse_edge(edge):
    return int(edge[1]), int(edge[3]), int(edge[5])


if __name__ == "__main__":
    main()
