from tqdm import tqdm
from __compute_polarization__ import get_polarization
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values


def greedy(k, graph_in, first_k_flag):

    """
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
        positive_nodes = positive_nodes[:100]
        negative_nodes = negative_nodes[:100]

    for i in range(k):
        edges, polarization = greedy_batch(k, graph, positive_nodes, negative_nodes)

        edge_1 = edges[0][0][0]
        edge_2 = edges[0][0][1]

        graph.add_edge(edge_1, edge_2)
        k_items.append((edge_1, edge_2))

    return k_items, get_polarization(graph)


def greedy_batch(k, graph_in, positive_nodes, negative_nodes):
    graph = graph_in.copy()
    original_polarization = get_polarization(graph)
    addition_info = {}

    for node_pos in positive_nodes:
        for node_neg in tqdm(negative_nodes):

            edge_to_add = (node_pos[0], node_neg[0])

            # skip edge if the edge exists in the original graph
            if graph.has_edge(*edge_to_add):
                continue

            g_copy = graph.copy()
            graph.add_edges_from([edge_to_add])
            polarization_after_addition = get_polarization(g_copy)
            decrease = original_polarization - polarization_after_addition
            addition_info[edge_to_add] = decrease

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph)

    return k_items, polarization


def expressed(k, graph_in, mode):
    """
    :param k:
    :param graph_in:
    :param mode: 1 for distance, 2 for multiplication
    :return:
    """
    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    addition_info = {}

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    for node_pos in positive_nodes:
        for node_neg in negative_nodes:

            edge_to_add = (node_pos[0], node_neg[0])

            # skip edge if the edge exists in the original graph
            if graph.has_edge(*edge_to_add):
                continue

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])
            node_1 = nodeDict[node_pos[0]]['value']
            node_2 = nodeDict[node_neg[0]]['value']

            if mode == 1:
                val = abs(node_1 - node_2)
            else:
                val = node_1 * node_2

            addition_info[edge_to_add] = val

            if mode == 1:
                flag = True
            else:
                flag = False

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=flag)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph)

    return k_items, polarization
