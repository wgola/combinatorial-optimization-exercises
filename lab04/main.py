from Graph import Graph


def main():
    tests = int(input().strip())

    for i in range(tests):

        first_line = input().strip()
        nodes_count = int(first_line[2])

        graph = Graph(nodes_count)
        second_line = input().strip()

        edges = second_line.split(" ")
        for edge in edges:
            start, end, weight = parse_edge(edge)
            graph.add_edge(start, end, weight)

        graph.kruskal_algorithm("input" + str(i + 1))


def parse_edge(edge):
    return int(edge[1]), int(edge[3]), int(edge[5])


if __name__ == "__main__":
    main()
