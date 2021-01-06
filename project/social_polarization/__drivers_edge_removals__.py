from connect_opposing import brute_force_all_edges_removal
from __graph_properties__ import edges_centralities
from __helpers_general__ import format_edge_list
from __visualize__ import visualize_edge
import pprint


def edge_removals_driver(graph, name):
    edge_dict = brute_force_all_edges_removal(graph, f'{name}_edges.pickle', 0)
    decrease_dict = {}
    increase_dict = {}

    for decrease in edge_dict.keys():

        if decrease > 0:
            decrease_dict[decrease] = edge_dict[decrease]

        elif decrease < 0:
            increase_dict[decrease] = edge_dict[decrease]

        else:
            print("edge(s) that has not effect on polarization")
            print(edge_dict[decrease])

    top_decrease = edges_centralities(graph, edge_dict, 5, True)
    top_increase = edges_centralities(graph, edge_dict, 5, False)

    print("=================")
    pprint.pprint(top_decrease)
    print("-----------------")
    pprint.pprint(top_increase)
    print("=================")

    decrease_list_for_vis = format_edge_list(top_decrease)
    increase_list_for_vis = format_edge_list(top_increase)

    visualize_edge(graph, decrease_list_for_vis, "Edges that had the biggest decrease with removal",
                   "decrease_removal", name, 0)
    visualize_edge(graph, increase_list_for_vis, "Edges that had the biggest increase with removal",
                   "increase_removal", name, 0)
