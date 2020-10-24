import networkx as nx
from numpy import take
from tqdm import tqdm

from compute_polarization import get_polarization
from helpers import add_edges_and_count_polarization


def naive_algorithm(k, graph):

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

    k_items = sorted_edges[:5]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph)

    return k_items, polarization


def merge_pol_algorithm(k, graph):

    nodeDict = dict(graph.nodes(data=True))
    positive_dictionary = {}
    negative_dictionary = {}

    original_polarization = get_polarization(graph)

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

            if first_pass_polarization[i+1] < polarization_after_addition:
                break

            edges_to_add_list.append(edge_to_add)
            if len(edges_to_add_list) == k:
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization


def merge_pol_without_p_z(k, graph):

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
            distance_to_check = abs(positive_dictionary[i+1][1] - node_neg_value)

            if distance_to_check > distance_current:
                break

            edges_to_add_list.append(edge_to_add)
            if len(edges_to_add_list) == k:
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization