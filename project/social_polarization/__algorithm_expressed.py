from tqdm import tqdm

from __algorithm_expressed__batch import expressed_batch
from __helpers_general__ import add_edges_and_count_polarization
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

    edges_to_add_list = []

    start = time.time()

    g_copy = graph_in.copy()

    for edge in tqdm(range(max(k))):
        results, polarizations_from_batch, time_list = expressed_batch(k,
                                                                       g_copy,
                                                                       mode,
                                                                       expected_p_z_mode,
                                                                       probabilities_dictionary)

        edge_1 = results[0][0]
        edge_2 = results[0][1]

        g_copy.add_edge(edge_1, edge_2)
        edges_to_add_list.append((edge_1, edge_2))

    end = time.time()

    for k_edge in k:
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list[:k_edge], graph_in))

        print(edges_to_add_list[:k_edge])
        print(add_edges_and_count_polarization(edges_to_add_list[:k_edge], graph_in))
    max_edges_added = edges_to_add_list[:max(k)]

    return max_edges_added, polarizations, [end - start] * len(k)
