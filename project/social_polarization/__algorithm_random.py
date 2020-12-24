from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values
from tqdm import tqdm
import random
import time


def random_edge_addition(k, graph_in):
    nodeDict = dict(graph_in.nodes(data=True))
    different_opinions = []
    polarizations = []
    times = []

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    start = time.time()
    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#"):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos[0], node_neg[0])

            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue
            different_opinions.append(edge_to_add)

    end = time.time()

    for k_edge in k:
        # just create an array with the same time for every edge. (time here is constant)
        times.append(end - start)

        edges_to_add_list = random.choices(different_opinions, k=k_edge)

        # pass a graph in the helper that copies it
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

    return different_opinions, polarizations, times
