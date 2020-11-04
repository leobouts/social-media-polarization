import networkx as nx
from tqdm import tqdm

from compute_polarization import get_polarization
from helpers import add_edges_and_count_polarization


def greedy_algorithm(k, graph_in):
    graph = graph_in.copy()
    edges_to_add = list(nx.non_edges(graph))
    k_items = []

    for i in tqdm(range(k)):
        original_polarization = get_polarization(graph)
        addition_info = {}
        sorted_edges = []

        for edge in edges_to_add:
            g_copy = graph.copy()
            g_copy.add_edges_from([edge])

            polarization_after_addition = get_polarization(g_copy)
            decrease = original_polarization - polarization_after_addition
            addition_info[edge] = decrease

        sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

        k_items.append(sorted_edges[0])
        edge_1 = sorted_edges[0][0][0]
        edge_2 = sorted_edges[0][0][1]
        graph.add_edge(edge_1, edge_2)
        edges_to_add.pop(edges_to_add.index((edge_1, edge_2)))

    return k_items, get_polarization(graph)


def greedy_without_consideration_algorithm(k, graph_in):
    graph = graph_in.copy()
    edges_to_add = nx.non_edges(graph)
    original_polarization = get_polarization(graph)
    addition_info = {}

    for edge in tqdm(edges_to_add):
        g_copy = graph.copy()
        g_copy.add_edges_from([edge])
        polarization_after_addition = get_polarization(g_copy)
        decrease = original_polarization - polarization_after_addition
        addition_info[edge] = decrease

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph)

    if not polarization:
        print('bruh wtf')

    return k_items, polarization


def skip_algorithm(k, graph_in):
    graph = graph_in.copy()

    nodeDict = dict(graph.nodes(data=True))
    positive_dictionary = {}
    negative_dictionary = {}

    first_pass_polarization = []

    for node in nodeDict:
        node_value = nodeDict[node]['value']
        if node_value > 0:
            positive_dictionary[node] = node_value
        else:
            negative_dictionary[node] = node_value

    positive_dictionary = sorted(positive_dictionary.items(), key=lambda x: x[1], reverse=True)
    negative_dictionary = sorted(negative_dictionary.items(), key=lambda x: x[1], reverse=True)

    first_of_negative = negative_dictionary[0][0]

    edges_to_add_list = []

    for positive_opinion in positive_dictionary:
        g_copy = graph.copy()
        g_copy.add_edges_from([(positive_opinion[0], first_of_negative)])
        polarization_after_addition = get_polarization(g_copy)

        first_pass_polarization.append(polarization_after_addition)

    for i, node_pos in enumerate(positive_dictionary):
        for j, node_neg in enumerate(negative_dictionary):

            edge_to_add = (node_pos[0], node_neg[0])

            if i == len(positive_dictionary):
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])
            polarization_after_addition = get_polarization(g_copy)

            if first_pass_polarization[i + 1] < polarization_after_addition:
                break

            edges_to_add_list.append(edge_to_add)
            if len(edges_to_add_list) == k:
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization


def distance_algorithm(k, graph_in):
    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    positive_dictionary = {}
    negative_dictionary = {}

    for node in nodeDict:
        node_value = nodeDict[node]['value']
        if node_value > 0:
            positive_dictionary[node] = node_value
        else:
            negative_dictionary[node] = node_value

    positive_dictionary = sorted(positive_dictionary.items(), key=lambda x: x[1], reverse=True)
    negative_dictionary = sorted(negative_dictionary.items(), key=lambda x: x[1], reverse=True)

    edges_to_add_list = []

    for i, node_pos in enumerate(positive_dictionary):
        node_pos_value = node_pos[1]

        for j, node_neg in enumerate(negative_dictionary):

            node_neg_value = node_neg[1]
            edge_to_add = (node_pos[0], node_neg[0])

            if i == len(positive_dictionary):
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])

            distance_current = abs(node_pos_value - node_neg_value)
            distance_to_check = abs(positive_dictionary[i + 1][1] - node_neg_value)

            if distance_to_check > distance_current:
                break

            edges_to_add_list.append(edge_to_add)
            if len(edges_to_add_list) == k:
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization


def spanning_tree_algorithm(k, graph):

    g_complement = nx.complement(graph)
    nodeDict = dict(g_complement.nodes(data=True))
    # because node and edge data do not propagate in the nx.complement
    node_dict_for_data = dict(graph.nodes(data=True))

    for node in nodeDict:

        edges_of_this_node = g_complement.edges(node)

        for edge in edges_of_this_node:
            val_1 = node_dict_for_data[edge[0]]['value']
            val_2 = node_dict_for_data[edge[1]]['value']

            edge_weight = abs(abs(val_1) - abs(val_2))
            g_complement[edge[0]][edge[1]]['weight'] = edge_weight
