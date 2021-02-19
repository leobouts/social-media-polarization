from __compute_polarization__ import get_polarization
from __helpers_algorithm__ import get_first_top_k_positive_and_negative_opinions
from tqdm import tqdm
import random
import time


def random_edge_addition_different(k, graph_in):
    edges_to_add_list = []
    polarizations = [0]*len(k)
    edges_list = []

    start = time.time()

    initial_polarization, converged_opinions = get_polarization(graph_in)

    positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(len(converged_opinions),
                                                                                    converged_opinions)

    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#"):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos, node_neg)

            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue

            edges_list.append(edge_to_add)

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
