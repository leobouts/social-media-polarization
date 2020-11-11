import pprint
import time

import networkx as nx
from algorithms import greedy_without_consideration_algorithm, skip_algorithm, distance_algorithm, greedy_algorithm
from compute_polarization import get_polarization
from connect_opposing import brute_force_all_edges_removal
from helpers import format_edge_list, convert_dataset_to_gml
from perm import *
from properties import edges_centralities
from visualize import vis_graphs_heuristics, visualize_edge_removal


def load_graph(gml_file):
    """"
    Loads the graph from the gml_file that also have the values of expressed opinions. If these values
    are in the [0,1] the function can change them to [-1,1] by turning the zeros into negatives.

    :param gml_file: name of the stored values
    :param change_zeros_to_negatives: true/false

    :return: networkx graph
    """
    graph = nx.read_gml(gml_file, label='id')

    # make sure we convert the graph to a simple one if the data
    # contain multiple same edges (multigraph)
    # also multigraph data must have the flag "multigraph 1" in the header
    # to work

    graph = nx.Graph(graph)

    value_dictionary = nx.get_node_attributes(graph, 'value')

    conservative_liberal_convert = ['../datasets/books.gml', '../datasets/ClintonTrump.gml']

    zero_value_convert = ["../datasets/GermanWings.gml",
                          "../datasets/beefban.gml",
                          "../datasets/sxsw.gml",
                          ]

    if gml_file in conservative_liberal_convert:
        # empty dictionary
        attrs = {}

        for key, value in value_dictionary.items():
            # c = conservative, l=liberal, n=neutral

            if value_dictionary[key] == "c":
                value_dictionary[key] = 1

            elif value_dictionary[key] == "l":
                value_dictionary[key] = -1

            else:
                value_dictionary[key] = 0

            d = {key: {'value': value_dictionary[key]}}
            attrs.update(d)

        nx.set_node_attributes(graph, attrs)

    if gml_file in zero_value_convert:

        # get the values of the new graph in a dictionary
        value_dictionary = nx.get_node_attributes(graph, 'value')

        # opinions vary from 0 to 1, find all zero occurences
        zero_indices = [k for (k, v) in value_dictionary.items() if v == 0]

        # empty dictionary
        attrs = {}

        # create the dictionary that will update 0 nodes to -1
        for obj in zero_indices:
            d = {obj: {'value': -1}}
            attrs.update(d)

        # se the new opinion values
        nx.set_node_attributes(graph, attrs)

        # get the values of the new graph in a dictionary
        value_dictionary = nx.get_node_attributes(graph, 'value')

    list_of_graph_values = list(value_dictionary.values())

    graph = attach_values_from_list_to_graph(graph, list_of_graph_values)

    # print(list(graph.nodes(data=True)))
    # print(nx.info(graph))
    # print(get_polarization(graph))

    return graph


def attach_values_from_list_to_graph(g, values):
    """
    attaches values to each node of a graph
    ------------------------------------------------------
    :param g: networkx graph
    :param values: list of values of each node
    :return: networkx graph with attributes named 'value'.
    Each node now has their opinion stored.
    """

    attrs = {}

    for i, node in enumerate(g.nodes):
        attrs[node] = {'value': values[i]}

    # set the new opinion values
    nx.set_node_attributes(g, attrs)

    return g


def heuristics_driver(k):
    available_datasets = ['karate', 'books', 'polblogs', 'GermanWings', 'beefban', 'sxsw', 'ClintonTrump']
    #available_datasets = ['ClintonTrump']

    results = {}
    karate_normalised = False

    skip_merge_list = ['ClintonTrump', 'sxsw']
    skip_greedy_list = ['ClintonTrump', 'sxsw', 'polblogs', 'beefban']

    for ds in available_datasets:

        graph = load_graph(f'../datasets/{ds}.gml')

        # if ds == 'karate' and not karate_normalised:
        #     karate_normalised = True
        #
        #     values = [graph.nodes[i]["value"] for i in graph.nodes()]
        #
        #     norm = np.linalg.norm(values)
        #     normal_array = values / norm
        #
        #     print(values)
        #     print(normal_array)
        #
        #     nx.set_node_attributes(graph, normal_array, "values")

        greedy_polarization_decrease_list = []
        greedy_time = []

        greedy_without_polarization_decrease_list = []
        greedy_without_time = []

        merge_polarization_decrease_list = []
        merge_time = []

        distance_polarization_decrease_list = []
        distance_time = []

        list_of_decreases = [greedy_polarization_decrease_list,
                             greedy_without_polarization_decrease_list,
                             merge_polarization_decrease_list,
                             distance_polarization_decrease_list]

        list_of_times = [greedy_time,
                         greedy_without_time,
                         merge_time,
                         distance_time]

        list_of_labels = ["Greedy",
                          "Greedy Batch",
                          "Skip",
                          "Distance"]

        for k_edges in k:

            if ds not in skip_greedy_list:
                greedy_start = time.time()
                greedy_results, greedy_polarization = greedy_algorithm(k_edges, graph)
                greedy_polarization_decrease_list.append(greedy_polarization)
                greedy_end = time.time()
                greedy_elapsed = greedy_end - greedy_start
                greedy_time.append(greedy_elapsed)
                results[f'naive_{ds}'] = {'result_dictionary': greedy_results, 'time': greedy_elapsed,
                                          'polarization': greedy_polarization}

                greedy_without_start = time.time()
                greedy_without_results, greedy_without_polarization = greedy_without_consideration_algorithm(k_edges, graph)
                greedy_without_polarization_decrease_list.append(greedy_without_polarization)
                greedy_without_end = time.time()
                greedy_without_elapsed = greedy_without_end - greedy_without_start
                greedy_without_time.append(greedy_without_elapsed)
                results[f'naive_{ds}'] = {'result_dictionary': greedy_without_results, 'time': greedy_without_elapsed,
                                          'polarization': greedy_without_polarization}

            if ds not in skip_merge_list:
                merge_start = time.time()
                merge_results, merge_polarization = skip_algorithm(k_edges, graph)
                merge_polarization_decrease_list.append(merge_polarization)
                merge_end = time.time()
                merge_elapsed = merge_end - merge_start
                merge_time.append(merge_elapsed)
                results[f'merge_{ds}'] = {'result_dictionary': merge_results, 'time': merge_elapsed,
                                          'polarization': merge_polarization}

            distance_start = time.time()
            distance_results, distance_polarization = distance_algorithm(k_edges, graph)
            distance_polarization_decrease_list.append(distance_polarization)
            distance_end = time.time()
            distance_elapsed = distance_end - distance_start
            distance_time.append(distance_elapsed)
            results[f'distance_{ds}'] = {'result_dictionary': distance_results, 'time': distance_elapsed,
                                         'polarization': distance_polarization}

        print(ds)
        print(greedy_polarization_decrease_list)
        print(greedy_time)
        print(greedy_without_polarization_decrease_list)
        print(greedy_without_time)
        print(merge_polarization_decrease_list)
        print(merge_time)
        print(distance_polarization_decrease_list)
        print(distance_time)

        empty_indexes = [i for i, x in enumerate(list_of_decreases) if not x]

        list_of_decreases = [i for j, i in enumerate(list_of_decreases) if j not in empty_indexes]
        list_of_times = [i for j, i in enumerate(list_of_times) if j not in empty_indexes]
        list_of_labels = [i for j, i in enumerate(list_of_labels) if j not in empty_indexes]

        vis_graphs_heuristics(k, list_of_decreases,
                              list_of_labels,
                              f"{ds} Polarization Decrease",
                              "Number of Edges",
                              "π(z)")

        vis_graphs_heuristics(k,
                              list_of_times,
                              list_of_labels,
                              f"{ds} Time Elapsed",
                              "Number of Edges",
                              "Seconds")


def edge_removals(graph, name):
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

    visualize_edge_removal(graph, decrease_list_for_vis, "Edges that had the biggest decrease with removal",
                           "decrease_removal")
    visualize_edge_removal(graph, increase_list_for_vis, "Edges that had the biggest increase with removal",
                           "increase_removal")


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


def main():
    # --------------------------------------- #
    #     convert datasets to gml             #
    # --------------------------------------- #

    convert_datasets_driver()

    # --------------------------------------- #
    # function that supports Lemma 3.1        #
    # --------------------------------------- #

    # find_increase_in_graphs_with_addition()

    # --------------------------------------- #
    #      Graph Init                         #
    #      options: karate, polblogs, books   #
    #      ClintonTrump, GermanWings          #
    #      k: top-k edges to add              #
    # --------------------------------------- #

    #name = 'sxsw'
    #graph = load_graph(f'../datasets/{name}.gml')
    #print(get_polarization(graph))

    # --------------------------------------- #
    #     Heuristics experiment               #
    # --------------------------------------- #

    k = [1, 5, 10, 15, 20]
    heuristics_driver(k)

    # --------------------------------------- #
    #     Fully connected for lemma 5.1       #
    # --------------------------------------- #

    # fully_connected_graph = make_graph_fully_connected(graph)
    # print(get_polarization(fully_connected_graph))

    # --------------------------------------- #
    #              edge removals              #
    # --------------------------------------- #

    # edge_removals(graph, name)

    # costly brute force, polblogs dataset needs arround 200 hours to check, karate is ok.
    # find biggest and smallest decrease of nodes after adding an edge.
    # However this measures the state of the nodes and not the edges.
    # decreasing_dictionary = brute_force_opposing_views(graph, f'{name}.pickle', 0)
    # top_decrease, small_decrease = centralities(graph, decreasing_dictionary, 5)

    # visualize_graph(graph, top_decrease, small_decrease, 'addition')
    # print(top_decrease)


if __name__ == "__main__":
    main()
