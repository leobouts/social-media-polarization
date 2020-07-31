from compute_polarization import get_polarization
from tqdm import tqdm
import networkx as nx
import pickle


def brute_force_opposing_views(graph, pickle_name):
    """""
    This method brute forces all opposing opinion nodes and find the decrease of the network
    by adding every possible edge between them. (1 edge at a time). Also stores the resulting
    dictionary in a pickle file

    ##todo maybe implement 3,4,.. edge additions, too much time tho :/

    -----------------------------------------------------------------------------------------
    :param pickle_name: name of the file that the results will be stored
    :param graph: networkx graph
    :return: dictionary that holds information about the decrease after adding an edge
    """

    value_dictionary = nx.get_node_attributes(graph, 'value')

    positive_indices = [k for (k, v) in value_dictionary.items() if v == 1]

    negative_indices = [k for (k, v) in value_dictionary.items() if v == -1]

    # create all edge pairs to be added
    all_pairs = [[pos_node, neg_node] for pos_node in positive_indices for neg_node in negative_indices]

    # clean duplicate edges if exist, [a,b]==[b,a]
    all_pairs = list({tuple(sorted(item)) for item in all_pairs})

    initial_polarization = get_polarization(graph)

    # holds values of decrease fo each addition
    difference = {}

    for i in tqdm(range(len(all_pairs))):

        # add a new addition every time
        g_copy = graph.copy()

        g_copy.add_edge(all_pairs[i][0], all_pairs[i][1])

        # check if the addition already exist in the graph, every addition must NOT be
        # an edge that exists inside the graph beforehand.
        # exist = True : all edge_additions does not exist in the current graph
        # exist = False: at least one edge addition in edge_additions exist in the current graph

        new_pol = get_polarization(g_copy)

        difference[abs(initial_polarization - new_pol)] = {'addition': f"{all_pairs[i][0]}->{all_pairs[i][1]}"}

    # Store data (serialize)
    with open(pickle_name, 'wb') as handle:
        pickle.dump(difference, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #for key in sorted(difference):
    #   print("%s: %s" % (key, difference[key]))

    return difference


def connect_opposing_seperated_in_areas(graph):

    value_dictionary = nx.get_node_attributes(graph, 'value')

    positive_indices = [k for (k, v) in value_dictionary.items() if v == 1]

    negative_indices = [k for (k, v) in value_dictionary.items() if v == -1]

    max_of_positive = max(positive_indices)
    max_of_negative = min(negative_indices)

    ## todo

