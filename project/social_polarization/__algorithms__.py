import time

import networkx as nx
from tqdm import tqdm
from __compute_polarization__ import get_polarization
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values


def greedy(k, graph_in, batch_flag, first_k_flag, expected_p_z_mode):
    """
    :param batch_flag:
    :param k:
    :param graph_in:
    :param first_k_flag:
    :return:
    """

    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    polarizations = []
    times = []
    k_items = []

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    if batch_flag:
        k_items, polarizations, elapsed = greedy_batch(k, graph_in, positive_nodes, negative_nodes, False)
        times = [elapsed for i in range(len(k))]

        return k_items, polarizations, times

    for k_edge in tqdm(k, ascii="~~~~~~~~~~~~~~~#"):
        k_items = []

        if first_k_flag:
            positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

            positive_nodes = positive_nodes[:k_edge]
            negative_nodes = negative_nodes[:k_edge]

        start = time.time()
        for i in range(k_edge):
            edges, polarization, elapsed = greedy_batch(k, graph, positive_nodes, negative_nodes, True)

            edge_1 = edges[0][0][0]
            edge_2 = edges[0][0][1]

            graph.add_edge(edge_1, edge_2)
            k_items.append((edge_1, edge_2))

        polarizations.append(add_edges_and_count_polarization(k_items, graph_in))
        end = time.time()
        times.append(end - start)

    return k_items, polarizations, times


def greedy_batch(k, graph_in, positive_nodes, negative_nodes, expected_p_z_mode, verbose):

    """
    Greedy batch finds the best edge to add according to the polarization decrease ammong all
    different opinions. It is also used with an expected mode to consider the addition of edges
    considering additional information e.g. common neighbors

    :param k: List that contains all the top-k edge additions we want to examine, e.g
    [5, 10, 15, 20]
    :param graph_in: Networkx graph that we want to examine
    :param positive_nodes: Nodes that have a z value of (0,1]
    :param negative_nodes: Nodes that have a z value od [-1,0)
    :param expected_p_z_mode: Expected problem function defintion. Available modes:
    'common_neighbors'
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

    original_polarization = get_polarization(graph_in)
    polarizations = []
    addition_info = {}

    start = time.time()
    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#", disable=verbose):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos[0], node_neg[0])

            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue

            # check how much the polarization was reduced in comparison with the original graph
            g_copy = graph_in.copy()
            g_copy.add_edges_from([edge_to_add])

            polarization_after_addition = get_polarization(g_copy)
            decrease = original_polarization - polarization_after_addition

            # addition_info is computed differently if we considering
            # the expected addition problem, bellow we consider the following
            # cases

            if expected_p_z_mode == 'common_neighbors':

                common_neighbors = nx.common_neighbors(graph_in, node_pos[0], node_neg[0])
                addition_info[edge_to_add] = decrease*common_neighbors

            else:
                # considering the initial problem of just the polarization decrease
                addition_info[edge_to_add] = decrease

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

    return sorted_edges, polarizations, elapsed


def expressed(k, graph_in, mode):
    """
    :param k:
    :param graph_in:
    :param mode: True for absolute distance, False for multiplication
    :return:
    """

    nodeDict = dict(graph_in.nodes(data=True))
    addition_info = {}
    polarizations = []
    times = []
    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    start = time.time()
    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#"):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos[0], node_neg[0])

            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue

            node_1 = nodeDict[node_pos[0]]['value']
            node_2 = nodeDict[node_neg[0]]['value']

            if mode == 1:
                val = abs(node_1 - node_2)
            else:
                val = node_1 * node_2

            addition_info[edge_to_add] = val
    end = time.time()

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=mode)

    for k_edge in k:
        # just create an array with the same time for every edge. (time here is constant)
        times.append(end - start)

        edges_to_add_list = [edge[0] for edge in sorted_edges[:k_edge]]

        # pass a graph in the helper that copies it
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list, graph_in))

    return sorted_edges, polarizations, times
