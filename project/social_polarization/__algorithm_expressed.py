from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values
from __compute_polarization__ import get_polarization
from tqdm import tqdm
import networkx as nx
import time


def expressed(k, graph_in, mode, expected_p_z_mode, probabilities_dictionary):
    """
    :param probabilities_dictionary:
    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param mode: 'Distance' for absolute distance, 'Multiplication' for multiplication
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    to not consider it the flag 'Ignore' can be passed.
    :return:
    1) sorted_edges, a list of all the edges proposed sorted by their decrease or
    expected decrease.

    2) polarizations, a list contain the polarization after the addition of the top-k edges that were proposed
     each time. top-k edges are given as an input in the parameter k above.

    3) elapsed time of the algorithms.
    """

    nodeDict = dict(graph_in.nodes(data=True))
    addition_info = {}
    polarizations = []
    times = []

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)
    initial_polarization, converged_opinions = get_polarization(graph_in)

    start = time.time()
    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#"):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos[0], node_neg[0])

            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue

            node_1 = converged_opinions[node_pos[0]]
            node_2 = converged_opinions[node_neg[0]]

            if mode == "Distance":
                val = abs(node_1 - node_2)
                mode_flag = True
            else:
                val = node_1 * node_2
                mode_flag = False

            # addition_info is computed differently if we considering
            # the expected addition problem, bellow we consider the following
            # cases

            if expected_p_z_mode == 'common_neighbors':

                common_neighbors = list(nx.common_neighbors(graph_in, node_pos[0], node_neg[0]))
                val = val * len(common_neighbors)

            elif expected_p_z_mode == 'Jaccard_coefficient':
                Jaccard = list(nx.jaccard_coefficient(graph_in, [(node_pos[0], node_neg[0])]))
                val = val * Jaccard[0][2]

            elif expected_p_z_mode == 'Adamic_addar_index':
                Adamic = list(nx.adamic_adar_index(graph_in, [(node_pos[0], node_neg[0])]))
                val = val * Adamic[0][2]

            elif expected_p_z_mode == 'Embeddings':
                probability = probabilities_dictionary[edge_to_add]
                val = val * probability

            addition_info[edge_to_add] = val

    end = time.time()

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=mode_flag)

    # compute all the polarization decreases for every K we have given as input.
    for k_edge in k:
        # just create an array with the same time for every edge. (time here is constant)
        times.append(end - start)

        edges_to_add_list = [edge[0] for edge in sorted_edges[:k_edge]]
        # pass a graph in the helper that copies it
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

    return sorted_edges, polarizations, times
