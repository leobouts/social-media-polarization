import time

from algorithms import naive_algorithm, merge_pol_algorithm, merge_pol_without_p_z
from connect_opposing import brute_force_opposing_views, brute_force_all_edges_removal
from compute_polarization import get_polarization
from make_graph_fully_connected import make_graph_fully_connected
from perm import *
from properties import centralities, edges_centralities, create_edge_list
from visualize import visualize_graph
import networkx as nx
import pprint


def load_graph(gml_file, change_zeros_to_negatives):
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

    if gml_file == 'books.gml':
        # empty dictionary

        attrs = {}

        for key, value in value_dictionary.items():
            # c = conservative, l=liberal, n=neutral

            if value_dictionary[key] == 'c':
                value_dictionary[key] = 1

            elif value_dictionary[key] == 'l':
                value_dictionary[key] = -1

            else:
                value_dictionary[key] = 0

            d = {key: {'value': value_dictionary[key]}}
            attrs.update(d)

        nx.set_node_attributes(graph, attrs)

    if change_zeros_to_negatives:

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
    available_datasets = ['karate', 'books', 'polblogs']
    results = {}

    for ds in available_datasets:
        graph = load_graph(f'{ds}.gml', True)

        if ds != 'polblogs':
            naive_start = time.time()
            naive_results, naive_polarization = naive_algorithm(k, graph)
            naive_end = time.time()
            naive_elapsed = naive_end - naive_start
            results[f'naive_{ds}'] = {'result_dictionary': naive_results, 'time': naive_elapsed,
                                      'polarization': naive_polarization}

            merge_start = time.time()
            merge_results, merge_polarization = merge_pol_algorithm(k, graph)
            merge_end = time.time()
            merge_elapsed = merge_end - merge_start
            results[f'merge_{ds}'] = {'result_dictionary': merge_results, 'time': merge_elapsed,
                                      'polarization': merge_polarization}

            distance_start = time.time()
            distance_results, distance_polarization = merge_pol_without_p_z(k, graph)

            distance_end = time.time()
            distance_elapsed = distance_end - distance_start
            results[f'distance_{ds}'] = {'result_dictionary': distance_results, 'time': distance_elapsed,
                                         'polarization': distance_polarization}

    pprint.pprint(results)


def main():
    # --------------------------------------- #
    # function that supports Lemma 3.1        #
    # --------------------------------------- #

    # find_increase_in_graphs_with_addition()

    # --------------------------------------- #
    #      Graph Init                         #
    #      options: karate, polblogs, books   #
    #      k: top-k edges to add              #
    # --------------------------------------- #

    name = 'karate'
    graph = load_graph(f'{name}.gml', True)
    k = 5
    print(get_polarization(graph))
    name = 'books'
    graph = load_graph(f'{name}.gml', True)
    print(get_polarization(graph))

    # --------------------------------------- #
    #     Heuristics experiment               #
    # --------------------------------------- #

    heuristics_driver(k)

    # print("ddd")
    # force_example(graph)
    # print("hh")
    # fully_connected_graph = make_graph_fully_connected(graph)
    # print(get_polarization(fully_connected_graph))

    # costly brute force, polblogs dataset needs arround 200 hours to check, karate is ok.
    # find biggest and smallest decrease of nodes after adding an edge.
    # However this measures the state of the nodes and not the edges.
    # decreasing_dictionary = brute_force_opposing_views(graph, f'{name}.pickle', 0)
    # top_decrease, small_decrease = centralities(graph, decreasing_dictionary, 5)

    # visualize_graph(graph, top_decrease, small_decrease, 'addition')
    # print(top_decrease)

    # edge_dict = brute_force_all_edges_removal(graph, f'{name}_edges.pickle', 0)
    # top_edge_decrease, small_edge_decrease = edges_centralities(graph, edge_dict, 5)
    #
    # top_list_for_vis = create_edge_list(top_edge_decrease)
    # small_list_for_vis = create_edge_list(small_edge_decrease)
    #
    # visualize_graph(graph, top_list_for_vis, small_list_for_vis, 'removal')

    # pprint.pprint(small_edge_decrease)


if __name__ == "__main__":
    main()
