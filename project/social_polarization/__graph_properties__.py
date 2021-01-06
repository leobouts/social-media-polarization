import networkx as nx
from __helpers_general__ import print_res


def centralities(graph, decrease_dictionary, no_of_nodes):
    """
    Given a network x graph and information about the polarization
    finds the closeness, betweenness and Eigen centrality of the nodes that were connected
    and had the biggest and the smallest decrease

    --------------------------------------------------------------------------------
    :param graph: network x graph
    :param decrease_dictionary: dictionary that has information about the polarization for every edge addition
    :param no_of_nodes: number of nodes that the function will print for biggest and smallest decrease
    :return: 1. list of edges with the biggest polarization index decrease
             2. list of edges with the smallest polarization index decrease
             example: ['6,30', '7,30', '17,26', '17,24', '17,30']
    """

    sorted_dict = sorted(decrease_dictionary)

    smallest_decrease = sorted_dict[:no_of_nodes]
    biggest_decrease = sorted_dict[-no_of_nodes:]

    top_decrease_nodes = []
    small_decrease_nodes = []
    biggest_decrease_edges = []
    smallest_decrease_edges = []

    for value in biggest_decrease:
        decrease = decrease_dictionary[value]
        edge_added = decrease['addition'].replace('->', ',')
        biggest_decrease_edges.append(edge_added)
        nodes = edge_added.split(',')
        top_decrease_nodes.append(nodes[0])
        top_decrease_nodes.append(nodes[1])

    for value in smallest_decrease:
        decrease = decrease_dictionary[value]
        edge_added = decrease['addition'].replace('->', ',')
        smallest_decrease_edges.append(edge_added)
        nodes = edge_added.split(',')
        small_decrease_nodes.append(nodes[0])
        small_decrease_nodes.append(nodes[1])

    # remove duplicate nodes
    top_decrease_nodes = list(dict.fromkeys(top_decrease_nodes))
    small_decrease_nodes = list(dict.fromkeys(small_decrease_nodes))

    # map the to int so they can be sorted and accessed
    top_decrease_nodes = list(map(int, top_decrease_nodes))
    small_decrease_nodes = list(map(int, small_decrease_nodes))

    top_decrease_nodes = sorted(top_decrease_nodes[:no_of_nodes])
    small_decrease_nodes = sorted(small_decrease_nodes[:no_of_nodes])

    # holds centrality values of every node
    closeness_c = nx.closeness_centrality(graph)
    betweenness_c = nx.betweenness_centrality(graph)
    eigen_centrality = nx.eigenvector_centrality(graph)

    top_node_closeness_c = [closeness_c[node] for node in top_decrease_nodes]
    top_node_betweenness = [betweenness_c[node] for node in top_decrease_nodes]
    top_node_eigen = [eigen_centrality[node] for node in top_decrease_nodes]

    small_node_closeness_c = [closeness_c[int(node)] for node in small_decrease_nodes]
    small_node_betweenness = [betweenness_c[int(node)] for node in small_decrease_nodes]
    small_node_eigen = [eigen_centrality[node] for node in small_decrease_nodes]

    print_res(top_decrease_nodes, top_node_closeness_c, top_node_betweenness, top_node_eigen, 'Largest')
    print_res(small_decrease_nodes, small_node_closeness_c, small_node_betweenness, small_node_eigen, 'Smallest')

    return biggest_decrease_edges, smallest_decrease_edges


def edges_centralities(graph, dictionary, no_of_nodes, mode):
    """
    Computes the edge centralities of the graph and returns the top #no_of_nodes
    with the biggest and the smallest polarization decrease after removing an edge
    in their graph.
    :param graph: netrowkx graph
    :param dictionary: holds the decrease of the polarization with edge removals
    for every available edge in the graph
    :param no_of_nodes: number of bigger/smaller decrease with removal
    in polarization that I want to keep
    :param mode: Boolean-> True for decrease, False for increase
    :return: 1 dictionary for increase or decrease with edge centralities
    """
    sorted_dict = sorted(dictionary, reverse=mode)

    sorted_dict = sorted_dict[:no_of_nodes]
    betweenness_c = nx.edge_betweenness_centrality(graph)
    dictionary_to_return = {}
    top = {}

    for value in sorted_dict:
        decrease = dictionary[value]
        edge_removed = decrease['edge_removal']
        top[value] = {'edge_removed': edge_removed}

    for value in top:
        edge_to_get_val = top[value]['edge_removed']
        edge_bet_centrality = betweenness_c[edge_to_get_val]
        sign = dictionary[value]['multiplication']
        addition = dictionary[value]['addition']
        dictionary_to_return[value] = {'edge_removed': edge_to_get_val,
                                       'edge_centrality': edge_bet_centrality,
                                       'sign': sign,
                                       'addition': addition}

    return dictionary_to_return
