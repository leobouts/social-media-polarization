import networkx as nx

from __algorithm_helpers import iterate_over_different_opinions, get_first_top_k_positive_and_negative_opinions
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values
from __compute_polarization__ import get_polarization
from tqdm import tqdm
import time


def first_top_greedy_batch(k, graph_in, expected_p_z_mode, verbose, probabilities_dictionary):
    """
    Greedy batch finds the best edge to add according to the polarization decrease among all
    different opinions. It is also used with an expected mode to consider the addition of edges
    considering additional information e.g. common neighbors

    :param probabilities_dictionary:
    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param positive_nodes: Nodes that have a z value of (0,1]
    :param negative_nodes: Nodes that have a z value od [-1,0)
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    to not consider it the flag 'Ignore' can be passed.
    :param verbose: disabling or enabling the tqdm progress bar output to the console.
    do not change. GBatch is also used on greedy so it is used to disable the inner progress
    bar when we run the greedy algorithm.
    :return:

    1) sorted_edges, a list of all the edges proposed sorted by their decrease or
    expected decrease.

    2) polarizations, a list contain the polarization after the addition of the top-k edges that were proposed
     each time. top-k edges are given as an input in the parameter k above.

    3) elapsed time of the algorithm.
    """

    original_polarization, converged_opinions = get_polarization(graph_in)
    polarizations = []

    start = time.time()

    for k_edge in k:

        positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(graph_in, k_edge)

        addition_info = iterate_over_different_opinions(graph_in,
                                                        positive_nodes,
                                                        negative_nodes,
                                                        original_polarization,
                                                        expected_p_z_mode,
                                                        probabilities_dictionary, verbose)

        sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

        edges_to_add_list = [edge[0] for edge in sorted_edges[:k_edge]]
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

    end = time.time()
    elapsed = end - start

    return sorted_edges, polarizations, [elapsed] * len(k)


