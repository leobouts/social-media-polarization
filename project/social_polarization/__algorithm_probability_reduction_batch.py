from __helpers_algorithm__ import iterate_over_different_opinions, get_first_top_k_positive_and_negative_opinions
from __helpers_general__ import add_edges_and_count_polarization
from __compute_polarization__ import get_polarization
import time


def p_reduction(k, graph_in, mode, expected_p_z_mode, probabilities_dictionary):

    polarizations = []

    if mode == "Distance" or mode =="pReduction":
        reverse_flag = True
    else:
        reverse_flag = False

    edges_to_add_list = []

    start = time.time()

    g_copy = graph_in.copy()

    initial_polarization, converged_opinions = get_polarization(g_copy)
    positive_nodes, negative_nodes = get_first_top_k_positive_and_negative_opinions(len(converged_opinions),
                                                                                    converged_opinions)

    addition_info = iterate_over_different_opinions(g_copy,
                                                    positive_nodes,
                                                    negative_nodes,
                                                    initial_polarization,
                                                    converged_opinions,
                                                    mode,
                                                    expected_p_z_mode,
                                                    probabilities_dictionary,
                                                    True)

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=reverse_flag)

    # consider only edges that do not already exist
    for edge in sorted_edges:

        if not g_copy.has_edge(*edge[0]):
            edges_to_add_list.append(edge[0])

    end = time.time()

    for k_edge in k:
        polarizations.append(add_edges_and_count_polarization(edges_to_add_list[:k_edge], graph_in))

    max_edges_added = edges_to_add_list[:max(k)]

    return max_edges_added, polarizations, [end - start] * len(k)
