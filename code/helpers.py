from compute_polarization import get_polarization


def add_edges_and_count_polarization(edges_list, graph):

    graph.add_edges_from(edges_list)

    return get_polarization(graph)
