import pprint
import time

from __algorithms__ import *
from connect_opposing import brute_force_all_edges_removal
from __load_graph_data__ import load_graph
from __helpers__ import convert_dataset_to_gml, format_edge_list, check_for_same_results
from __graph_properties__ import edges_centralities
from __visualize__ import *


def heuristic_driver(k, datasets, algorithms):
    """
    :param k: list that contains all the different top-k additions we want to add to the graph
    :param datasets: a list containing the string names of the datasets we want to examine
    :param algorithms: a list containing the string names of the algorithms we wan to run on the datasets
    :return: dictionary info that has all the information about every experiment. It uses
     the this key to store informattion ---> info[{algorithm}_{dataset}_{edges}] = {...}
    """
    info = {}
    print("===============================================")
    for ds in datasets:
        graph = load_graph(f'../datasets/{ds}.gml')
        total_decreases = []
        total_times = []

        for algorithm in algorithms:
            print(f'\r Now in --> Dataset: {ds}, algorithm: {algorithm}', end='', flush=True)

            decrease_list = []
            time_list = []

            # append initial polarization for the graph output
            decrease_list.append(get_polarization(graph))
            for k_edges in k:
                polarization = 0
                results = []

                start = time.time()
                if algorithm == 'Greedy':
                    results, polarization = greedy(k_edges, graph)
                elif algorithm == 'GBatch':
                    results, polarization = greedy_batch(k_edges, graph)
                elif algorithm == 'Skip':
                    results, polarization = skip(k_edges, graph)
                elif algorithm == 'Distance':
                    results, polarization = distance(k_edges, graph)
                elif algorithm == 'DME':
                    results, polarization = expressed(k_edges, graph, 1)
                elif algorithm == 'MME':
                    results, polarization = expressed(k_edges, graph, 1)

                decrease_list.append(polarization)
                end = time.time()
                elapsed = end - start
                time_list.append(elapsed)
                index = f'{algorithm}_{ds}_{k_edges}'
                info[index] = {'result_dictionary': results,
                               'time': elapsed,
                               'polarization': polarization}

            total_decreases.append(decrease_list)
            total_times.append(time_list)

        decreases_checked, labels_checked = check_for_same_results(total_decreases, algorithms, 1)

        k_copy = k.copy()
        k_copy.insert(0, 0)

        vis_graphs_heuristics(k_copy,
                              decreases_checked,
                              labels_checked,
                              f"{ds} Polarization Decrease",
                              "Number of Edges Added",
                              "π(z)",
                              0)

        times_checked, time_labels_checked = check_for_same_results(total_times, algorithms, 0)

        vis_graphs_heuristics(k,
                              times_checked,
                              time_labels_checked,
                              f"{ds} Time Elapsed",
                              "Number of Edges Added",
                              "Seconds",
                              1)
    print("\r Finished.")

    return info


def convert_datasets_driver():
    base_data_dir = "/Users/leonidas/desktop/February 21/thesis/Data/"

    communities_values = ["Germanwings/communities_germanwings",
                          "Beefban/communities_beefban",
                          "sxsw/communities_sxsw",
                          "Elections/ClintonTrumpCommunities3000"]

    communities_connections = ["Germanwings/germanwings_followers_network_part_largest_CC",
                               "Beefban/beefban_followers_network_part_largest_CC",
                               "sxsw/sxsw_followers_network_part_largest_CC",
                               "Elections/ClintonTrumpEdges3000"]

    names_to_save = ["GermanWings.gml", "beefban.gml", "sxsw.gml", "ClintonTrump.gml"]

    for i in range(len(communities_values)):
        val = base_data_dir + communities_values[i]
        ed = base_data_dir + communities_connections[i]
        convert_dataset_to_gml(val, ed, names_to_save[i])


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
                   "decrease_removal", 0)
    visualize_edge(graph, increase_list_for_vis, "Edges that had the biggest increase with removal",
                   "increase_removal", 0)
