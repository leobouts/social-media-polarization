from __helpers_algorithm__ import iterate_over_different_opinions, get_first_top_k_positive_and_negative_opinions
from __helpers_general__ import add_edges_and_count_polarization
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

    if mode == "Distance":
        reverse_flag = True
    else:
        reverse_flag = False

    edges_to_add_list = []

    start = time.time()

    g_copy = graph_in.copy()

    for i in tqdm(range(max(k)), ascii="~~~~~~~~~~~~~~~#"):

        initial_polarization, converged_opinions = get_polarization(g_copy)

        positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(len(converged_opinions),
                                                                                        converged_opinions)
        addition_info = iterate_over_different_opinions(g_copy,
                                                        positive_nodes,
                                                        negative_nodes,
                                                        initial_polarization,
                                                        converged_opinions,
                                                        mode,
                                                        expected_p_z_mode,
                                                        probabilities_dictionary,
                                                        True)

        sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=reverse_flag)

        for edge in sorted_edges:

            if edge[0] not in edges_to_add_list:
                edges_to_add_list.append(edge[0])
                g_copy.add_edges_from([edge[0]])
                break

    end = time.time()

    for k_edge in k:
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list[:k_edge], graph_in))

    return edges_to_add_list, polarizations, [end - start] * len(k)
