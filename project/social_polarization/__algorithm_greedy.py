from __algorithm_greedy_batch import greedy_batch
from __algorithm_helpers import get_first_top_k_positive_and_negative_opinions
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values
from __compute_polarization__ import get_polarization
from tqdm import tqdm
import time


def greedy(k, graph_in, first_k_flag, expected_p_z_mode, probabilities_dictionary):
    """
    :param probabilities_dictionary:
    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param first_k_flag: if True performs a greedy search on the first KxK nodes according to z value.
    :param batch_flag: if True runs only the GBatch algorithm
    :param expected_p_z_mode: Expected problem function definition. Available modes:
    'common_neighbors', 'Jaccard_coefficient', 'Adamic_addar_index', 'Embeddings'
    :return:
    1) k_items, a list of all the edges proposed sorted by their decrease or
    expected decrease. They already sorted from the greedy_batch function so they don't need to be sorted
    here

    2) polarizations, a list contain the polarization after the addition of the top-k edges that were proposed
     each time. top-k edges are given as an input in the parameter k above.

    3) times, elapsed times of the algorithm for each k.
    """
    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    polarizations = []
    times = []
    k_items = []

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    # Greedy and FKGreedy runs here,
    # they use GBatch K times.

    for k_edge in tqdm(k, ascii="~~~~~~~~~~~~~~~#"):

        k_items = []
        graph = graph_in.copy()

        if first_k_flag:
            # The FKGreedy algorithm reduces the space by running
            # the Greedy algorithm using only the first KxK nodes
            positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(graph_in, k_edge)

        start = time.time()
        for i in range(k_edge):
            edges, polarization, elapsed = greedy_batch(k, graph, positive_nodes, negative_nodes, expected_p_z_mode,
                                                        True, probabilities_dictionary)

            edge_1 = edges[0][0][0]
            edge_2 = edges[0][0][1]

            graph.add_edge(edge_1, edge_2)
            k_items.append((edge_1, edge_2))

        polarizations.append(add_edges_and_count_polarization(k_items, graph))
        end = time.time()
        times.append(end - start)

    return k_items, polarizations, times