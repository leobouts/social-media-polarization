import networkx as nx
from tqdm import tqdm

from __compute_polarization__ import get_polarization
from __helpers__ import get_positive_and_negative_values


def iterate_over_different_opinions(graph_in, positive_nodes, negative_nodes, original_polarization, expected_p_z_mode,
                                    probabilities_dictionary, verbose):
    addition_info = {}

    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#", disable=verbose):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos[0], node_neg[0])
            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue

            # check how much the polarization was reduced in comparison with the original graph
            g_copy = graph_in.copy()
            g_copy.add_edges_from([edge_to_add])

            polarization_after_addition, converged_opinions = get_polarization(g_copy)
            decrease = original_polarization - polarization_after_addition

            # addition_info is computed differently if we considering
            # the expected addition problem, bellow we consider the following
            # cases

            if expected_p_z_mode == 'common_neighbors':
                common_neighbors = list(nx.common_neighbors(graph_in, node_pos[0], node_neg[0]))
                addition_info[edge_to_add] = decrease * len(common_neighbors)

            elif expected_p_z_mode == 'Jaccard_coefficient':
                Jaccard = list(nx.jaccard_coefficient(graph_in, [(node_pos[0], node_neg[0])]))
                addition_info[edge_to_add] = decrease * Jaccard[0][2]

            elif expected_p_z_mode == 'Adamic_addar_index':
                Adamic = list(nx.adamic_adar_index(graph_in, [(node_pos[0], node_neg[0])]))
                addition_info[edge_to_add] = decrease * Adamic[0][2]

            elif expected_p_z_mode == 'Embeddings':
                probability = probabilities_dictionary[edge_to_add]
                addition_info[edge_to_add] = decrease * probability

            else:
                # considering the initial problem of just the polarization decrease
                addition_info[edge_to_add] = decrease

    return addition_info


def get_first_top_k_positive_and_negative_opinions(graph_in, k_edge):

    nodeDict = dict(graph_in.nodes(data=True))

    positive_nodes, negative_nodes = get_positive_and_negative_values(nodeDict)

    pol, converged_opinions = get_polarization(graph_in)

    index_list = [i for i in range(len(converged_opinions))]

    converged_opinions, index_list = zip(*sorted(zip(converged_opinions, index_list)))

    positive_indexes = [i for i in index_list if i in positive_nodes]
    negative_indexes = [i for i in index_list if i in negative_nodes]

    positive_nodes = positive_indexes[:k_edge]
    negative_nodes = negative_indexes[:k_edge]

    return positive_nodes, negative_nodes
