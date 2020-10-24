import networkx as nx
from tqdm import tqdm

from compute_polarization import get_polarization


def naive_algorithm(graph):

    edges_to_add = nx.non_edges(graph)
    original_polarization = get_polarization(graph)
    addition_info = {}
    for edge in tqdm(edges_to_add):

        g_copy = graph.copy()

        g_copy.add_edges_from([edge])
        polarization_after_addition = get_polarization(g_copy)
        decrease = original_polarization - polarization_after_addition
        addition_info[edge] = {'polarization_decrease': decrease}

    return addition_info


def merge_pol_algorithm(graph):

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

    first_of_negative = negative_dictionary[0][1]

    for positive_opinion in positive_dictionary:

        g_copy = graph.copy()

        g_copy.add_edges_from([(positive_opinion[1], first_of_negative)])
        polarization_after_addition = get_polarization(g_copy)

        first_pass_polarization.append(polarization_after_addition)

