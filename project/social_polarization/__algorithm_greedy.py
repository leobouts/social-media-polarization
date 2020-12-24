from __helpers__ import add_edges_and_count_polarization
from __algorithm_greedy_batch import greedy_batch
from tqdm import tqdm
import time


def greedy(k, graph_in, expected_p_z_mode, probabilities_dictionary):
    """
    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    :param probabilities_dictionary:
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

    # Even though we could just run greedy one time with the max number of
    # edges we want, we have to run him for every first-top edges to get his
    # running times.

    for k_edge in tqdm(k, ascii="~~~~~~~~~~~~~~~#"):

        k_items = []

        # copy the graph so we won't alter it
        graph = graph_in.copy()

        start = time.time()

        for i in range(k_edge):

            edges, polarization, elapsed = greedy_batch(k, graph, expected_p_z_mode, True, probabilities_dictionary)

            edge_1 = edges[0][0][0]
            edge_2 = edges[0][0][1]

            graph.add_edge(edge_1, edge_2)
            k_items.append((edge_1, edge_2))

        polarizations.append(add_edges_and_count_polarization(k_items, graph))
        end = time.time()

        times.append(end - start)

    return k_items, polarizations, times
