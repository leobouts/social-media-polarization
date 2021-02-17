from __compute_polarization__ import get_polarization
import networkx as nx
import random
import time


def random_edge_addition(k, graph_in):

    edges_to_add_list = []
    polarizations = [0]*len(k)
    edges_list = list(nx.non_edges(graph_in))

    start = time.time()

    # run 20 times to sample and then average the results of random edge selection
    for i in range(20):
        for j, k_edge in enumerate(k):

            edges_to_add_list = random.sample(edges_list, k_edge)

            g_copy = graph_in.copy()
            g_copy.add_edges_from(edges_to_add_list)

            polarizations[j] += get_polarization(g_copy)[0]

    end = time.time()
    elapsed = end - start

    averaged_polarizations = [x / 20 for x in polarizations]

    return edges_to_add_list, averaged_polarizations, [elapsed] * len(k)
