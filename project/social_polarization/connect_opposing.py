from __compute_polarization__ import get_polarization
from tqdm import tqdm
import networkx as nx
import pickle


def brute_force_opposing_views(graph, pickle_name, verbose):
    """""
    This method brute forces all opposing opinion nodes and find the decrease of the network
    by adding every possible edge between them. (1 edge at a time). Also stores the resulting
    dictionary in a pickle file

    #todo 1. maybe implement 3,4,.. edge additions, too much time for larger networks (even small ones)
    #todo 2. implement it for graphs that have intermediate values not only -1 and 1 (also need dataset?)
    ------------------------------------------------------------------------------------------------------
    :param pickle_name: name of the file that the results will be stored
    :param graph: networkx graph
    :param verbose: =1 prints result to terminal, =0 hides result from terminal
    :return: dictionary that holds information about the decrease after adding an edge
    example : "{0.01938319984207737: {'addition': '15->20'}, ...}"
    """

    value_dictionary = nx.get_node_attributes(graph, 'value')

    positive_indices = [k for (k, v) in value_dictionary.items() if v == 1]

    negative_indices = [k for (k, v) in value_dictionary.items() if v == -1]

    # create all edge pairs to be added
    all_pairs = [[pos_node, neg_node] for pos_node in positive_indices for neg_node in negative_indices]

    # clean duplicate edges if exist, [a,b]==[b,a]
    all_pairs = list({tuple(sorted(item)) for item in all_pairs})

    initial_polarization, converged_opinions = get_polarization(graph)

    # holds values of decrease for each addition
    difference = {}

    for i in tqdm(range(len(all_pairs))):

        g_copy = graph.copy()

        # add a new addition every time
        g_copy.add_edge(all_pairs[i][0], all_pairs[i][1])

        # get the new polarization after addition
        new_pol, converged_opinions = get_polarization(g_copy)

        # compute and store decrease

        difference[abs(initial_polarization - new_pol)] = {'addition': f"{all_pairs[i][0]}->{all_pairs[i][1]}"}

    # store data (serialize) into pickle file
    with open(f"../pickles/{pickle_name}", 'wb') as handle:
        pickle.dump(difference, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # prints to terminal
    if verbose:
        for key in sorted(difference):
            print("%s: %s" % (key, difference[key]))

    return difference


def brute_force_all_edges_removal(graph, pickle_name, verbose):
    """""
        This method brute forces all opposing opinion nodes and find the decrease of the network
        by REMOVING every possible edge between them. (1 edge at a time). Also stores the resulting
        dictionary in a pickle file. It is not so costly as the edge additions derived from the fact
        that we have to remove only existing edges and not all possible combinations
        ------------------------------------------------------------------------------------------------------
        :param pickle_name: name of the file that the results will be stored
        :param graph: networkx graph
        :param verbose: =1 prints result to terminal, =0 hides result from terminal
        :return: dictionary that holds information about the decrease after adding an edge
        """
    graph_edges = graph.edges()
    graph_polarization, converged_opinions = get_polarization(graph)
    nodeDict = dict(graph.nodes(data=True))
    difference = {}

    for edge in tqdm(graph_edges):

        g_copy = graph.copy()
        # unpacks e from an edge tuple
        g_copy.remove_edge(*edge)
        # get new polarization after deleting an edge
        new_polarization, converged_opinions = get_polarization(g_copy)

        # get data from the nodes attached to this edge
        node_a_polarization = nodeDict[edge[0]]['value']
        node_b_polarization = nodeDict[edge[1]]['value']

        mul = node_a_polarization * node_b_polarization
        add = node_a_polarization + node_b_polarization

        difference[graph_polarization - new_polarization] = {'edge_removal': edge,
                                                                  'multiplication': mul,
                                                                  'addition': add}

    # store data (serialize) into pickle file
    with open(f"../pickles/{pickle_name}", 'wb') as handle:
        pickle.dump(difference, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # prints to terminal
    if verbose:
        print("Difference with edge removals:")
        print("==============================")
        for key in sorted(difference):
            print("%s: %s" % (key, difference[key]))

    return difference
