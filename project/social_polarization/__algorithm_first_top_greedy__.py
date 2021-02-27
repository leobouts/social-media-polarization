from __helpers_algorithm__ import iterate_over_different_opinions, get_first_top_k_positive_and_negative_opinions
from __compute_polarization__ import get_polarization
from tqdm import tqdm
import time

from __helpers_general__ import add_edges_and_count_polarization


def first_top_greedy(k, graph_in, expected_p_z_mode, probabilities_dictionary):
    """
    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    :param probabilities_dictionary: probabilities coming from embeddings
    :return:
    1) k_items, a list of all the edges proposed sorted by their decrease or
    expected decrease. They already sorted from the greedy_batch function so they don't need to be sorted
    here

    2) polarizations, a list contain the polarization after the addition of the top-k edges that were proposed
     each time. top-k edges are given as an input in the parameter k above.

    3) times, elapsed times of the algorithm for each k.
    """
    polarizations = []
    times = []
    k_items = []
    addition_return_info = []

    # copy the graph so we won't alter it
    graph = graph_in.copy()

    start = time.time()

    for i in tqdm(range(max(k)), ascii="~~~~~~~~~~~~~~~#"):

        polarization, converged_opinions = get_polarization(graph)
        positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(max(k), converged_opinions)

        addition_info = iterate_over_different_opinions(graph,
                                                        positive_nodes,
                                                        negative_nodes,
                                                        polarization,
                                                        converged_opinions,
                                                        'Not expressed',
                                                        expected_p_z_mode,
                                                        probabilities_dictionary,
                                                        True)

        sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

        graph.add_edges_from([sorted_edges[0][0]])

        k_items.append(sorted_edges[0][0])
        addition_return_info.append(sorted_edges[0])

    end = time.time()

    for k_edge in k:
        polarizations.append(add_edges_and_count_polarization(k_items[:k_edge], graph_in))
        times.append(end - start)

    return k_items, polarizations, times, addition_return_info
