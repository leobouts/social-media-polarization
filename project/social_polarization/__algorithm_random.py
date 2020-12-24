from __helpers__ import add_edges_and_count_polarization
import networkx as nx
import random
import time


def random_edge_addition(k, graph_in):

    polarizations = []
    start = time.time()

    edges_list = list(nx.non_edges(graph_in))

    for k_edge in k:

        edges_to_add_list = random.choices(edges_list, k=k_edge)

        # pass a graph in the helper that copies it
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

    end = time.time()
    elapsed = end - start

    return edges_to_add_list, polarizations, [elapsed] * len(k)
