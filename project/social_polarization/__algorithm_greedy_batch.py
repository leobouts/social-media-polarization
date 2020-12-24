from __algorithm_helpers import iterate_over_different_opinions
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values
from __compute_polarization__ import get_polarization
import time


def greedy_batch(k, graph_in, expected_p_z_mode, verbose,
                 probabilities_dictionary):
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

    nodeDict = dict(graph_in.nodes(data=True))
    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    start = time.time()

    addition_info = iterate_over_different_opinions(graph_in,
                                                    positive_nodes,
                                                    negative_nodes,
                                                    original_polarization,
                                                    expected_p_z_mode,
                                                    probabilities_dictionary, verbose)
    end = time.time()
    elapsed = end - start

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

    # compute all the polarization decreases for every K we have given as input.
    for k_edge in k:
        # GBatch computes all the edges at once so we can check the first k
        # at once with sorted_edges[:k_edge].
        edges_to_add_list = [edge[0] for edge in sorted_edges[:k_edge]]

        # pass a graph in the helper method (copies it)
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

    return sorted_edges, polarizations, [elapsed] * len(k)
