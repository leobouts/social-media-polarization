from __compute_polarization__ import get_polarization
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values


def greedy(k, graph_in, batch_flag, first_k_flag,):
    """
    :param batch_flag:
    :param k:
    :param graph_in:
    :param first_k_flag:
    :return:
    """

    graph = graph_in.copy()
    k_items = []
    nodeDict = dict(graph.nodes(data=True))

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    if first_k_flag:
        positive_nodes = positive_nodes[:k]
        negative_nodes = negative_nodes[:k]

    if batch_flag:
        k_items, polarization = greedy_batch(k, graph_in, positive_nodes, negative_nodes)
        return k_items, polarization

    for i in range(k):
        edges, polarization = greedy_batch(k, graph, positive_nodes, negative_nodes)

        edge_1 = edges[0][0][0]
        edge_2 = edges[0][0][1]

        graph.add_edge(edge_1, edge_2)
        k_items.append((edge_1, edge_2))

    return k_items, get_polarization(graph)


def greedy_batch(k, graph_in, positive_nodes, negative_nodes):
    """
    :param k:
    :param graph_in:
    :param positive_nodes:
    :param negative_nodes:
    :return:
    """
    original_polarization = get_polarization(graph_in)
    addition_info = {}

    for node_pos in positive_nodes:
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
            addition_info[edge_to_add] = decrease

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph_in.copy())

    return k_items, polarization


def expressed(k, graph_in, mode):
    """
    :param k:
    :param graph_in:
    :param mode: True for absolute distance, False for multiplication
    :return:
    """

    nodeDict = dict(graph_in.nodes(data=True))
    addition_info = {}

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    for node_pos in positive_nodes:
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

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=mode)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]

    # pass a graph copy so the addition will not alter the graph outside
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph_in.copy())

    return k_items, polarization
