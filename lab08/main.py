from tasks import tasks
import utils as u


if __name__ == "__main__":
    g = u.setup_graph(tasks)

    u.draw_activity_on_node_network(g)

    u.calculate_earliest_start_times(g)

    u.calculate_latest_start_and_rest_times(g)

    u.print_network_data(g)

    edges = u.find_critical_path(g)

    u.draw_critical_path(g, edges)

    u.draw_schedule(g)
