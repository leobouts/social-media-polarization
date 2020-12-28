from __algorithm_helpers import iterate_over_different_opinions, get_first_top_k_positive_and_negative_opinions
from __helpers__ import add_edges_and_count_polarization
from __compute_polarization__ import get_polarization
import time


def first_top_greedy_batch(k, graph_in, expected_p_z_mode, probabilities_dictionary):
    """
    Greedy batch finds the best edge to add according to the polarization decrease among all
    different opinions. It is also used with an expected mode to consider the addition of edges
    considering additional information e.g. common neighbors

    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    to not consider it the flag 'Ignore' can be passed.
    :param probabilities_dictionary:

    :return:

    1) sorted_edges, a list of all the edges proposed sorted by their decrease or
    expected decrease.

    2) polarizations, a list contain the polarization after the addition of the top-k edges that were proposed
     each time. top-k edges are given as an input in the parameter k above.

    3) elapsed time of the algorithm.
    """

    original_polarization, converged_opinions = get_polarization(graph_in)
    polarizations = []
    sorted_edges = []
    times = []

    for k_edge in k:
        start = time.time()

        positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(k_edge, converged_opinions)

        addition_info = iterate_over_different_opinions(graph_in,
                                                        positive_nodes,
                                                        negative_nodes,
                                                        original_polarization,
                                                        converged_opinions,
                                                        'Not expressed',
                                                        expected_p_z_mode,
                                                        probabilities_dictionary,
                                                        True)

        sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

        edges_to_add_list = [edge[0] for edge in sorted_edges[:k_edge]]

        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

        end = time.time()
        elapsed = end - start
        times.append(elapsed)

    return sorted_edges, polarizations, times
