from __compute_polarization__ import get_polarization
import networkx as nx
import random
import time


def random_edge_addition(k, graph_in):
    edges_to_add_list = []
    polarizations = []
    start = time.time()

    edges_list = list(nx.non_edges(graph_in))

    for k_edge in k:
        edges_to_add_list = random.sample(edges_list, k_edge)

        g_copy = graph_in.copy()
        g_copy.add_edges_from(edges_to_add_list)

        polarizations.append(get_polarization(g_copy)[0])

    end = time.time()
    elapsed = end - start

    return edges_to_add_list, polarizations, [elapsed] * len(k)
