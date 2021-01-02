from __algorithm_expressed import expressed
from __algorithm_first_top_greedy import first_top_greedy
from __algorithm_first_top_greedy_batch import first_top_greedy_batch
from __algorithm_random import random_edge_addition
from __algorithm_random_different_opinions import random_edge_addition_different
from __compute_polarization__ import get_polarization
from __format_datasets__ import get_nodes_and_values_from_nx_to_txt, convert_dataset_to_gml
from __helpers__ import format_edge_list, \
    check_for_same_results
from connect_opposing import brute_force_all_edges_removal
from __graph_properties__ import edges_centralities
from __graph_embeddings__ import graph_embeddings
from __load_graph_data__ import load_graph
from __algorithm_greedy import *
from __visualize__ import *
import pickle
import pprint


def algorithms_driver(k, datasets, algorithms, expected_mode):
    """
    :param expected_mode:
    :param k: list that contains all the different top-k additions we want to add to the graph
    :param datasets: a list containing the string names of the datasets we want to examine
    :param algorithms: a list containing the string names of the algorithms we wan to run on the datasets
    :return: dictionary info that has all the information about every experiment. It uses
             this key to store information ---> info[{algorithm}_{dataset}_{edges}] = {...}
    """

    info = {}

    print("====================================================")

    for ds in datasets:

        graph = load_graph(f'../datasets/{ds}.gml')

        total_decreases = []
        total_times = []
        polarizations = []
        results = []
        time_list = []
        probabilities_dictionary = {}

        if expected_mode != 'Ignore':
            results, probabilities = graph_embeddings(ds, 0)

            probabilities_dictionary = {results[i]: probabilities[i] for i in range(len(results))}

        for algorithm in algorithms:

            print(f'\r Now in --> Dataset: {ds}, algorithm: {algorithm}')
            time.sleep(1)

            # append initial polarization for the graph output
            pol, converged_opinions = get_polarization(graph)
            decrease_list = [pol]

            if algorithm == 'Greedy':
                results, polarizations, time_list = greedy(k, graph, expected_mode, probabilities_dictionary)

            elif algorithm == 'GBatch':
                results, polarizations, time_list = greedy_batch(k, graph, expected_mode, False,
                                                                 probabilities_dictionary)

            elif algorithm == 'FTGreedy':
                results, polarizations, time_list = first_top_greedy(k, graph, expected_mode, probabilities_dictionary)

            elif algorithm == 'FTGreedyBatch':
                results, polarizations, time_list = first_top_greedy_batch(k, graph, expected_mode,
                                                                           probabilities_dictionary)

            elif algorithm == 'Expressed Distance':
                results, polarizations, time_list = expressed(k, graph, 'Distance', expected_mode,
                                                              probabilities_dictionary)

            elif algorithm == 'Expressed Multiplication':
                results, polarizations, time_list = expressed(k, graph, 'Multiplication', expected_mode,
                                                              probabilities_dictionary)

            elif algorithm == 'Random':
                results, polarizations, time_list = random_edge_addition(k, graph)

            elif algorithm == 'Random different':
                results, polarizations, time_list = random_edge_addition_different(k, graph)

            decrease_list = decrease_list + polarizations

            for i, k_edges in enumerate(k):
                index = f'{algorithm}_{ds}_{k_edges}'
                info[index] = {'result_dictionary': results[:k_edges],
                               'time': time_list[i],
                               'polarization': decrease_list[i + 1]}

            total_decreases.append(decrease_list)
            total_times.append(time_list)

        decreases_checked, labels_checked = check_for_same_results(total_decreases, algorithms, 1)

        # store data (serialize) into pickle file
        with open(f"../pickles/{ds}/{ds}_info", 'wb') as handle:
            pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(f"../pickles/{ds}/{ds}_decreases_checked_pol", 'wb') as handle:
            pickle.dump(decreases_checked, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(f"../pickles/{ds}/{ds}_labels_checked_pol", 'wb') as handle:
            pickle.dump(labels_checked, handle, protocol=pickle.HIGHEST_PROTOCOL)

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

        # store data (serialize) into pickle file
        with open(f"../pickles/{ds}/{ds}_times_checked", 'wb') as handle:
            pickle.dump(times_checked, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # store data (serialize) into pickle file
        with open(f"../pickles/{ds}/{ds}_labels_checked_time", 'wb') as handle:
            pickle.dump(time_labels_checked, handle, protocol=pickle.HIGHEST_PROTOCOL)

        vis_graphs_heuristics(k,
                              times_checked,
                              time_labels_checked,
                              f"{ds} Time Elapsed",
                              "Number of Edges Added",
                              "Seconds",
                              1)

        # store info into pickle file
        with open(f"../pickles/{ds}/{ds}_info", 'wb') as handle:
            pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)

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


def convert_networkx_to_txt_for_embeddings_driver():
    datasets = ['karate', 'polblogs', 'books', 'ClintonTrump', 'GermanWings', 'sxsw', 'beefban']

    for ds_name in datasets:
        graph = load_graph(f'../datasets/{ds_name}.gml')
        get_nodes_and_values_from_nx_to_txt(graph, ds_name)


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


def dataset_statistics_driver(datasets, verbose):
    info = {}

    for ds in datasets:
        graph = load_graph(f'../datasets/{ds}.gml')
        polarization, converged_opinions = get_polarization(graph)
        stats = nx.info(graph)

        if verbose:
            print(stats)
            print("Polarization:", end='')
            print(polarization)
            print("---------------------")

        info[ds] = {'polarization': polarization, 'info': stats}

    return info
