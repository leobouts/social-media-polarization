from numpy import linalg as LA
import networkx as nx


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


def print_res(nodes, closeness_c, betweenness_c, eigen_c, mode):
    """
    :param nodes: id of nodes, same index with the results
    :param closeness_c: list of closeness centralities of nodes
    :param betweenness_c: list of betweeness centralities of nodes
    :param eigen_c: list of Eigen centralities of nodes
    :param mode: just a string input for the print output, e.g. 'largest'
    :return: prints the results of the centralities methods and their norms
    """

    print(f"-----{mode} decrease------")
    print("Node ids:")
    print(nodes)
    print("Closeness centrality:")
    print(closeness_c)
    print("Norm:")
    print(LA.norm(closeness_c))
    print("============================")
    print("Betweeness centrality:")
    print(betweenness_c)
    print("Norm:")
    print(LA.norm(betweenness_c))
    print("============================")
    print("Eigen centrality:")
    print(eigen_c)
    print("Norm:")
    print(LA.norm(eigen_c))


def edges_centralities(graph, decrease_dictionary, no_of_nodes):
    """
    Computes the edge centralities of the graph and returns the top #no_of_nodes
    with the biggest and the smallest polarization decrease after removing an edge
    in their graph.
    :param graph: netrowkx graph
    :param decrease_dictionary: holds the decrease of the polarization with edge removals
    for every available edge in the graph
    :param no_of_nodes: number of bigger/smaller decrease with removal
    in polarization that I want to keep
    :return: 2 dictionaries, one for smaller one for bigger decrease of edge centralities
    """
    sorted_dict = sorted(decrease_dictionary)

    smallest_decrease = sorted_dict[:no_of_nodes]
    biggest_decrease = sorted_dict[-no_of_nodes:]

    top_decrease = {}
    small_decrease = {}

    for value in biggest_decrease:
        decrease = decrease_dictionary[value]
        edge_removed = decrease['edge_removal']
        top_decrease[value] = {'edge_removed': edge_removed}

    for value in smallest_decrease:
        decrease = decrease_dictionary[value]
        edge_removed = decrease['edge_removal']
        small_decrease[value] = {'edge_removed': edge_removed}

    betweenness_c = nx.edge_betweenness_centrality(graph)

    returned_edge_info_biggest_decrease = {}
    returned_edge_info_smallest_decrease = {}

    for value in top_decrease:
        edge_to_get_val = top_decrease[value]['edge_removed']
        edge_bet_centrality = betweenness_c[edge_to_get_val]
        sign = decrease_dictionary[value]['multiplication']
        addition = decrease_dictionary[value]['addition']
        returned_edge_info_biggest_decrease[value] = {'edge_removed': edge_to_get_val,
                                                      'edge_centrality': edge_bet_centrality,
                                                      'sign': sign,
                                                      'addition': addition}

    for value in small_decrease:
        edge_to_get_val = small_decrease[value]['edge_removed']
        edge_bet_centrality = betweenness_c[edge_to_get_val]
        sign = decrease_dictionary[value]['multiplication']
        addition = decrease_dictionary[value]['addition']
        returned_edge_info_smallest_decrease[value] = {'edge_removed': edge_to_get_val,
                                                       'edge_centrality': edge_bet_centrality,
                                                      'sign': sign,
                                                      'addition': addition}

    return returned_edge_info_biggest_decrease, returned_edge_info_smallest_decrease


def create_edge_list(dict_to_format):
    """

    :param dict_to_format: dictionary of type
    "0.04669391074827928: {'addition': 0,
                       'edge_centrality': 0.1272599949070537,
                       'edge_removed': (1, 32),
                       'sign': -1}}"
    :return: list of type ["1,2","2,3",..]
    """
    edge_list = []
    for keys in dict_to_format.keys():
        edge = str(dict_to_format[keys]['edge_removed']).replace(" ", "")
        edge = edge.replace("(", "")
        edge = edge.replace(")", "")
        edge_list.append(edge)

    return edge_list
