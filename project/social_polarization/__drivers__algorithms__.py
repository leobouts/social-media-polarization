from __algorithm_expressed import expressed
from __algorithm_probability_reduction_batch import p_reduction
from __algorithm_random_different_opinions__ import random_edge_addition_different
from __algorithm_first_top_greedy_batch__ import first_top_greedy_batch
from __algorithm_first_top_greedy__ import first_top_greedy
from __algorithm_random__ import random_edge_addition
from __compute_polarization__ import get_polarization
from __helpers_pickles__ import save_data_to_pickle
from __graph_embeddings__ import graph_embeddings
from __helpers_general__ import check_for_same_results
from __algorithm_expressed__batch import expressed_batch
from __load_graph_data__ import load_graph
from __algorithm_greedy__ import *
from __visualize__ import *


def algorithms_driver(k, datasets, algorithms, expected_mode, experiment_comment):
    """
    The result list is the max edges that each algorithm adds, for example if the experiment
    is conducted with the following list [5,10,15,20] the results will have the 20 edges that
    have been added. For later use you can just pick the first 5 if you need to check something
    on the 5 edges addition.

    :param experiment_comment:
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

        # holds probability for each edge that does not exist
        # key-> edge, value-> prob
        probabilities_dictionary = {}

        if expected_mode != 'Ignore' or 'pReduction' in algorithms:
            results, probabilities = graph_embeddings(ds, 0)

            probabilities_dictionary = {results[i]: probabilities[i] for i in range(len(results))}

        for algorithm in algorithms:

            print(f'\r Now in --> Dataset: {ds}, algorithm: {algorithm}')
            time.sleep(1)

            # append initial polarization for the graph output
            pol, converged_opinions = get_polarization(graph)
            decrease_list = [pol]

            if algorithm == 'Greedy':
                results, polarizations, time_list, addition_info = greedy(k, graph, expected_mode,
                                                                          probabilities_dictionary)

            elif algorithm == 'GBatch':
                results, polarizations, time_list, addition_info = greedy_batch(k, graph, expected_mode, False,
                                                                                probabilities_dictionary)
            elif algorithm == 'FTGreedy':
                results, polarizations, time_list, addition_info = first_top_greedy(k, graph, expected_mode,
                                                                                    probabilities_dictionary)

            elif algorithm == 'FTGreedyBatch':
                results, polarizations, time_list, addition_info = first_top_greedy_batch(k, graph, expected_mode,
                                                                                          probabilities_dictionary)
            elif algorithm == 'Expressed Distance':
                results, polarizations, time_list, addition_info = expressed(k, graph, 'Distance', expected_mode,
                                                                             probabilities_dictionary)
            elif algorithm == 'Expressed Multiplication':
                results, polarizations, time_list, addition_info = expressed(k, graph, 'Multiplication', expected_mode,
                                                                             probabilities_dictionary)
            elif algorithm == 'BExpressed Distance':
                results, polarizations, time_list, addition_info = expressed_batch(k, graph, 'Distance', expected_mode,
                                                                                   probabilities_dictionary)
            elif algorithm == 'BExpressed Multiplication':
                results, polarizations, time_list, addition_info = expressed_batch(k, graph, 'Multiplication',
                                                                                   expected_mode,
                                                                                   probabilities_dictionary)
            elif algorithm == 'pReduction':
                results, polarizations, time_list = p_reduction(k, graph, 'pReduction', expected_mode,
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

        save_data_to_pickle(data_to_write=[total_decreases, algorithms, decreases_checked, labels_checked, info,
                                           probabilities_dictionary, k],
                            atr_list=['decreases_pol', 'labels_pol', 'decreases_checked_pol', 'labels_checked_pol',
                                      'info', 'probabilities_dictionary', 'k_edge_number_addition_list'],
                            ds=ds,
                            experiment_comment=experiment_comment)

        k_copy = k.copy()
        k_copy.insert(0, 0)

        vis_graphs_heuristics(k_copy,
                              decreases_checked,
                              labels_checked,
                              f"{ds} Polarization Decrease",
                              "Number of Edges Added",
                              "π(z)",
                              0)

    return info


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
