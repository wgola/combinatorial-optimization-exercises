from NotDirectedGraph import NotDirectedGraph
from DirectedGraph import DirectedGraph


def main():
    graph = create_graph()
    option = choose_option()
    while option != "13":
        match option:
            case "1":
                graph.add_node()
                print("Dodano wierzchołek")
            case "2": remove_node(graph)
            case "3": add_edge(graph)
            case "4": remove_edge(graph)
            case "5": get_node_degree(graph)
            case "6": get_min_and_max_degree(graph)
            case "7": get_odd_and_even_nodes(graph)
            case "8": get_sorted_nodes_degrees(graph)
            case "9": get_c3(graph, "naive")
            case "10": get_c3(graph, "multiply")
            case "11": dfs(graph)
            case "12":
                path = graph.show_graph()
                print("Narysowany graf znajduje się w pliku '" + path + ".pdf'")

        print()
        option = choose_option()

    print("Kończenie działania...")


def create_graph():
    answer = input("Witaj! Wybierz opcje:\n"
                   + "1) Wczytaj graf z pliku\n"
                   + "2) Wprowadź graf ręcznie\n")

    while answer not in ["1", "2"]:
        answer = input("Wprowadź poprawną opcje!\n")

    if answer == "1":
        return get_graph_from_file()
    else:
        return enter_graph()


def get_graph_from_file():
    print("Plik powinien być przygotowany w nastepujący sposób:\n" +
          "Pierwsza linia - rodzaj grafu, 'skierowany' lub 'nieskierowany'\n" +
          "Druga linia - ilość wierzchołków w grafie,\n" +
          "Następne linie - krawędzie w formacie 'początek koniec', np. '1 2'")
    path = input("Podaj nazwę pliku:\n")

    try:
        file = open(path, "r")

        graph_type = file.readline()

        if graph_type not in ["skierowany\n", "nieskierowany\n"]:
            raise Exception()

        if graph_type == "skierowany\n":
            graph = DirectedGraph()
        else:
            graph = NotDirectedGraph()

        num_of_nodes = int(file.readline())

        for _ in range(num_of_nodes):
            graph.add_node()

        edges = file.readline()
        while edges:
            nodes = edges.split(" ")
            if len(nodes) == 2:
                start = int(nodes[0])
                end = int(nodes[1])
                graph.add_edge(start, end)
            edges = file.readline()

        print("Zakończono wczytywanie grafu")

        return graph
    except Exception as err:
        print(err.with_traceback())
        print("Błąd przetwarzania pliku!")
        exit()


def enter_graph():
    answer0 = input("Podaj rodzaj grafu:\n"
                    + "1) Graf nieskierowany\n"
                    + "2) Graf skierowany\n")

    while answer0 not in ["1", "2"]:
        answer0 = input("Wprowadź poprawną opcję!\n")

    if answer0 == "1":
        graph = NotDirectedGraph()
    else:
        graph = DirectedGraph()

    answer1 = input("Podaj ilość wierzchołków w grafie:\n")

    num_of_nodes = 0

    while True:
        try:
            num_of_nodes = int(answer1)
            if num_of_nodes < 0:
                raise Exception()
            break
        except:
            answer1 = input("Podaj poprawną liczbę!\n")

    for _ in range(num_of_nodes):
        graph.add_node()

    print("Wprowadż krawędzie (w formacie 'początek koniec', np. '1 2', aby zakończyć wprowadzanie wpisz 'KONIEC')")

    answer2 = input()
    while answer2 != "KONIEC":
        try:
            nodes = answer2.split(" ")
            start = int(nodes[0])
            end = int(nodes[1])
            graph.add_edge(start, end)
        except:
            print("Wprowadź poprawnie krawędź!")
        finally:
            answer2 = input()

    print("Zakończono wczytywanie grafu")
    return graph


def choose_option():
    answer = input("Wybierz działanie:\n"
                   + "1) Dodaj wierzhołek\n"
                   + "2) Usuń wierzhołek\n"
                   + "3) Dodaj krawędź\n"
                   + "4) Usuń krawędź\n"
                   + "5) Wyznacz stopień wierzchołka\n"
                   + "6) Wyznacz minimalny i maksymalny stopień grafu\n"
                   + "7) Wyznacz ilość parzystych i nieparzystych wierzchołków\n"
                   + "8) Wypisz posortowany ciąg stopni wierzchołków w grafie\n"
                   + "9) Znajdź cykl C3 (metoda naiwna)\n"
                   + "10) Znajdź cykl C3 (mnożenie macierzy)\n"
                   + "11) Przeszukaj graf algorytmem DFS\n"
                   + "12) Wyświetl graf\n"
                   + "13) Wyjdź z programu\n")

    if answer not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
        answer = input("Wprowadź poprawną opcje!\n")

    return answer


def remove_node(graph):
    answer = input("Podaj numer wierzchołka do usunięcia (licząc od 0):\n")

    while True:
        try:
            node = int(answer)
            graph.remove_node(node)
            print("Wierzchołek usunięty")
            break
        except:
            answer = input("Wprowadź poprawny wierzchołek!\n")


def add_edge(graph):
    answer = input(
        "Wprowadż krawędź (w formacie 'początek koniec', np. '1 2')\n")

    while True:
        try:
            nodes = answer.split(" ")
            start = int(nodes[0])
            end = int(nodes[1])
            graph.add_edge(start, end)
            print("Dodano krawędź")
            break
        except:
            answer = input("Wprowadź poprawnie krawędź!\n")


def remove_edge(graph):
    answer = input(
        "Wprowadż krawędź (w formacie 'początek koniec', np. '1 2')\n")

    while True:
        try:
            nodes = answer.split(" ")
            start = int(nodes[0])
            end = int(nodes[1])
            graph.remove_edge(start, end)
            print("Usunięto krawędź")
            break
        except:
            answer = input("Wprowadź poprawnie krawędź!\n")


def get_node_degree(graph):
    answer = input("Podaj numer wierzchołka (licząc od 0):\n")

    while True:
        try:
            node = int(answer)
            if isinstance(graph, NotDirectedGraph):
                degree = graph.get_node_degree(node)
                print("Stopień tego wierzchołka to: " + str(degree))
                break
            else:
                out_degree, in_degree = graph.get_node_degree(node)
                print("Stopień wchodzący wierzchołka to: " + str(in_degree) +
                      "\nStopień wychodzący wierzchołka to: " + str(out_degree))
                break
        except:
            answer = input("Wprowadź poprawny wierzchołek!\n")


def get_min_and_max_degree(graph):
    min_degree, max_degree = graph.get_graph_degree()
    print("Minimalny stopień grafu: " + str(min_degree) +
          "\nMaksymalny stopień grafu: " + str(max_degree))


def get_odd_and_even_nodes(graph):
    odd_nodes_count, even_nodes_count = graph.get_odd_and_even_nodes_count()
    print("Ilość nieparzystych wierzchołków: " + str(odd_nodes_count) +
          "\nIlość parzystych wierzchołków: " + str(even_nodes_count))


def get_sorted_nodes_degrees(graph):
    sorted_nodes_degrees = graph.get_nodes_degrees()
    print("Posortowany ciąg stopni wierzchołków w grafie: " + sorted_nodes_degrees)


def get_c3(graph, method):
    try:
        if method == "naive":
            result, nodes = graph.contains_c3_naive()
        else:
            result, nodes = graph.contains_c3_multiply()

        if result:
            print("Znaleziono cykl C3: ")
            print(str(nodes[0]) + " -> " +
                  str(nodes[1]) + " -> " + str(nodes[2]))
        else:
            print("Graf nie zawiera cyklu C3!")
    except:
        print("Graf musi być prosty!")


def dfs(graph):
    if isinstance(graph, DirectedGraph):
        print("Graf musi być nieskierowany!")
        return

    try:
        answer = input("Podaj numer początkowego wierzchołka (licząc od 0):\n")

        node = int(answer)
        order, filename = graph.dfs_spanning_tree(node)

        if order is None:
            print("Graf nie jest spójny!")
        else:
            print("Kolejność odwiedzanych wierzchołków: ")
            print(order)
            print("Narysowane drzewo spinającego znajduje się w pliku '" +
                  filename + ".pdf'")

    except Exception as err:
        if str(err) == "Graph is not simple!":
            print("Graf musi być prosty!")
        else:
            print("Podano niewłaściwy wierzchołek!")


if __name__ == "__main__":
    main()
