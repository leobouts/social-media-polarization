from __algorithm_helpers import iterate_over_different_opinions, get_first_top_k_positive_and_negative_opinions
from __helpers__ import add_edges_and_count_polarization
from __compute_polarization__ import get_polarization
from tqdm import tqdm
import time


def expressed(k, graph_in, mode, expected_p_z_mode, probabilities_dictionary):

    """
    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param mode: 'Distance' for absolute distance, 'Multiplication' for multiplication
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    to not consider it the flag 'Ignore' can be passed.
    :param probabilities_dictionary: probabilities coming from embeddings

    :return:
    1) sorted_edges, a list of all the edges proposed sorted by their decrease or
    expected decrease.

    2) polarizations, a list contain the polarization after the addition of the top-k edges that were proposed
     each time. top-k edges are given as an input in the parameter k above.

    3) elapsed time of the algorithms.
    """

    polarizations = []
    times = []

    if mode == "Distance":
        reverse_flag = True
    else:
        reverse_flag = False

    for k_edge in k:

        edges_to_add_list = []

        start = time.time()

        for i in tqdm(range(k_edge)):
            initial_polarization, converged_opinions = get_polarization(graph_in)

            positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(len(converged_opinions),
                                                                                            converged_opinions)
            addition_info = iterate_over_different_opinions(graph_in,
                                                            positive_nodes,
                                                            negative_nodes,
                                                            initial_polarization,
                                                            converged_opinions,
                                                            mode,
                                                            expected_p_z_mode,
                                                            probabilities_dictionary,
                                                            True)

            sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=reverse_flag)

            edges_to_add_list.append(sorted_edges[0][0])

        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))
        end = time.time()

        times.append(end - start)

    return edges_to_add_list, polarizations, times
