from __compute_polarization__ import get_polarization
from tqdm import tqdm


def iterate_over_different_opinions(graph_in,
                                    positive_nodes,
                                    negative_nodes,
                                    original_polarization,
                                    converged_opinions,
                                    mode,
                                    expected_p_z_mode,
                                    probabilities_dictionary,
                                    verbose):
    addition_info = {}

    for node_pos in tqdm(positive_nodes, ascii="~~~~~~~~~~~~~~~#", disable=verbose):
        for node_neg in negative_nodes:

            edge_to_add = (node_pos, node_neg)

            # skip edge if the edge exists in the original graph
            if graph_in.has_edge(*edge_to_add):
                continue

            if mode == "Distance":
                value = abs(converged_opinions[node_pos] - converged_opinions[node_neg])

            elif mode == "Multiplication":
                value = converged_opinions[node_pos] * converged_opinions[node_neg]

            else:

                # check how much the polarization was reduced in comparison with the original graph

                g_copy = graph_in.copy()
                g_copy.add_edges_from([edge_to_add])
                polarization_after_addition, converged_opinions = get_polarization(g_copy)

                if polarization_after_addition < original_polarization:
                    value = original_polarization - polarization_after_addition
                else:
                    # polarization increased
                    value = 999999

            # addition_info is computed differently if we considering
            # the expected addition problem

            if expected_p_z_mode == 'Embeddings':

                try:
                    probability = probabilities_dictionary[edge_to_add]

                    # some edges were  stored in reverse??
                except KeyError:
                    probability = probabilities_dictionary[(edge_to_add[1], edge_to_add[0])]

                addition_info[edge_to_add] = value * probability

            else:

                # considering the initial problem of just the polarization decrease
                addition_info[edge_to_add] = value

    return addition_info


def get_first_top_k_positive_and_negative_opinions(k_edge, converged_opinions):

    index_pos = []
    index_neg = []

    opinion_pos = []
    opinion_neg = []

    # separate them according to opinion (-,+)
    # dont use list.index(), some nodes have the exact z value
    # and will return the same index in the list providing us
    # with wrong edges to add bellow

    for opinion in converged_opinions:
        if opinion > 0:
            opinion_pos.append(opinion)
        else:
            opinion_neg.append(opinion)

    sorted_pos = sorted(opinion_pos, reverse=True)
    sorted_neg = sorted(opinion_neg)

    for pos_opinion in sorted_pos:
        index_pos.append(converged_opinions.index(pos_opinion))

    for neg_opinion in sorted_neg:
        index_neg.append(converged_opinions.index(neg_opinion))

    return index_pos[:k_edge], index_neg[:k_edge]
