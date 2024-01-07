import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.axes import Axes


def setup_graph(tasks: list[dict]):
    g = nx.DiGraph()

    for task in tasks:
        g.add_node(task["name"])

    for task in tasks:
        for preceding in task["preceding"]:
            g.add_edge(preceding, task["name"])

    g = nx.transitive_reduction(g)

    for task in tasks:
        g.nodes[task["name"]]["time"] = task["time"]

    for layer, nodes in enumerate(nx.topological_generations(g)):
        for node in nodes:
            g.nodes[node]["layer"] = layer

    return g


def draw_activity_on_node_network(g: nx.DiGraph):
    pos = nx.multipartite_layout(g, subset_key="layer")

    fig, ax = plt.subplots()
    nx.draw_networkx(g, pos=pos, ax=ax)
    fig.tight_layout()
    plt.show()


def calculate_earliest_start_times(g: nx.DiGraph):
    sorted_nodes = list(nx.topological_sort(g))

    for task in sorted_nodes:
        in_edges = g.in_edges(task)
        if len(in_edges) == 0:
            g.nodes[task]["earliest"] = 0
        else:
            max_earliest_time = 0
            for (start, end) in in_edges:
                max_earliest_time = max(
                    g.nodes[start]["earliest"] + g.nodes[start]["time"],
                    max_earliest_time
                )
            g.nodes[task]["earliest"] = max_earliest_time


def calculate_latest_start_and_rest_times(g: nx.DiGraph):
    sorted_nodes = list(nx.topological_sort(g))

    sorted_nodes.reverse()

    for task in sorted_nodes:
        out_edges = g.out_edges(task)
        if len(out_edges) == 0:
            g.nodes[task]["latest"] = g.nodes[task]["earliest"]
            g.nodes[task]["rest"] = g.nodes[task]["latest"] - \
                g.nodes[task]["earliest"]

        else:
            min_latest_time = float('inf')
            for (start, end) in out_edges:
                min_latest_time = min(
                    g.nodes[end]["latest"] - g.nodes[start]["time"],
                    min_latest_time
                )
            g.nodes[task]["latest"] = min_latest_time
            g.nodes[task]["rest"] = g.nodes[task]["latest"] - \
                g.nodes[task]["earliest"]


def print_network_data(g: nx.DiGraph):
    print("Zadanie | Czas zadania | Najwcześniejszy czas rozpoczęcia | Najpóżniejszy czas rozpoczęcia | Zapas")
    for (node, data) in g.nodes.items():
        print(node + " | " +
              str(data["time"]) + " | " +
              str(data["earliest"]) + " | " +
              str(data["latest"]) + " | " +
              str(data["rest"]))


def find_critical_path(g: nx.DiGraph):
    sorted_nodes = list(nx.topological_sort(g))

    sorted_nodes.reverse()

    node = None

    curr_end_time = float("-inf")
    for task in sorted_nodes:
        if g.nodes[task]["rest"] == 0 and g.nodes[task]["time"] + g.nodes[task]["earliest"] > curr_end_time:
            curr_end_time = g.nodes[task]["time"] + g.nodes[task]["earliest"]
            node = task

    edges = []

    while True:
        in_edges = g.in_edges(node)

        if len(in_edges) == 0:
            break

        curr_end_time = float("-inf")
        prev_node = None
        for (start, end) in in_edges:
            if g.nodes[start]["rest"] == 0 and g.nodes[start]["time"] + g.nodes[start]["earliest"] > curr_end_time:
                curr_end_time = g.nodes[task]["time"] + \
                    g.nodes[task]["earliest"]
                prev_node = start

        edges.insert(0, (prev_node, node))
        node = prev_node

    print("Ścieżka krytyczna:")
    for edge in edges:
        print(edge[0] + " -> ", end=" ")

    print(edges[-1][1])

    return edges


def draw_critical_path(g: nx.DiGraph, edges: list[tuple]):
    pos = nx.multipartite_layout(g, subset_key="layer")

    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(g, pos=pos, ax=ax)
    nx.draw_networkx_edges(g, pos=pos, ax=ax)

    nx.draw_networkx_edges(g, pos=pos, ax=ax, edgelist=edges, edge_color="r")
    nx.draw_networkx_labels(g, pos=pos)

    fig.tight_layout()
    plt.show()


def plot_rectangle(ax: Axes, x: int, y: int, width: int, height: int, label: str):
    r = Rectangle(
        (x, y),
        width,
        height,
        edgecolor="black"
    )
    ax.add_patch(r)

    rx, ry = r.get_xy()
    cx = rx + r.get_width() / 2.0
    cy = ry + r.get_height() / 2.0
    ax.annotate(
        label, (cx, cy),
        color='black',
        weight='bold',
        fontsize=10,
        ha='center',
        va='center'
    )


def draw_schedule(g: nx.DiGraph):
    fig, ax = plt.subplots()

    machines = [0]

    for (n, d) in g.nodes.items():
        no_free_machines = True
        for i in range(len(machines)):
            if machines[i] <= d["earliest"]:
                no_free_machines = False
                machines[i] = d["earliest"] + d["time"]
                plot_rectangle(ax, d["earliest"], i,
                               d["time"], 1, n)
                break

        if no_free_machines:
            machines.append(d["earliest"] + d["time"])
            plot_rectangle(ax, d["earliest"], len(machines)-1, d["time"],
                           1, n)

    plt.xlim([0, max(machines)])
    plt.ylim([0, len(machines)])
    plt.xticks([i for i in range(max(machines))])
    print("Długość uszeregowania: " + str(max(machines)))
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.xaxis.grid(color='gray', linestyle='dashed')
    plt.show()
