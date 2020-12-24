from __helpers__ import get_positive_and_negative_values
from __compute_polarization__ import get_polarization
import networkx as nx
from tqdm import tqdm


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

    # get the Z values
    pol, converged_opinions = get_polarization(graph_in)

    # just a list of length of nodes
    index_list = [i for i in range(len(converged_opinions))]

    # sort together the list of indexes with the list of z opinions
    converged_opinions, index_list = zip(*sorted(zip(converged_opinions, index_list)))

    index_pos = []
    converged_pos = []
    index_neg = []
    converged_neg = []

    # separate them according to opinion (-,+)
    for i in converged_opinions:

        if i > 0:
            converged_pos.append(i)
            index_pos.append(index_list[converged_opinions.index(i)])
        else:
            converged_neg.append(i)
            index_neg.append(index_list[converged_opinions.index(i)])

    # sort together the list of indexes with the list of z opinions now for each different opinion (-,+)
    converged_neg, index_neg = zip(*sorted(zip(converged_neg, index_neg)))
    converged_pos, index_pos = zip(*sorted(zip(converged_pos, index_pos)))

    # get the nodes we want from each opinions
    positive_nodes = index_pos[:k_edge]
    negative_nodes = index_neg[:k_edge]

    # add dummy tuple value so they can be used in the iterate_over_different_opinions method
    positive_nodes = [(node, 0) for node in positive_nodes]
    negative_nodes = [(node, 0) for node in negative_nodes]

    return positive_nodes, negative_nodes
