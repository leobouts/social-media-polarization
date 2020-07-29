import networkx as nx
import numpy as np
from tqdm import tqdm
from check_properties import check_properties
import pickle


def get_polarization(g):
    """"
    Creates the L+I matrix that is holded in variable f where L is the laplacian matrix of the graph.
    solves the (L+I)^-1 * S system and computes the polarization index value from the second norm of this
    array squared and normalized.

    --------------------------------------------------------------------------------------------------
    :param g: networkx graph with value attributes
    :return: Value of the polarization index
    """

    equations = []

    nodes = list(g.nodes)
    nodes = sorted(nodes)

    # check if the networkx graph has nodes named '1'
    # if so remove 1 so we can accept both naming conventions
    # and dont have a problem with linalg.solve

    if nodes[0] == 1:

        mapping = {}
        for i in nodes:
            mapping[i] = i - 1

        g = nx.relabel_nodes(g, mapping)

        nodes = list(g.nodes)
        nodes = sorted(nodes)

    # print(list(g.nodes(data=True)))

    values = list(nx.get_node_attributes(g, 'value').values())

    for node in nodes:
        neighbors = [n for n in g.neighbors(node)]
        neighbors = sorted(neighbors)

        # create the matrix according to adjacent nodes
        f = [-1 if a in neighbors else 0 for a in nodes]

        # +1 for the identity matrix
        f[node] = len(neighbors) + 1
        equations.append(f)

    a = np.array(equations)
    b = np.array(values)

    # solving (L+I)^-1 * S
    solutions = np.linalg.solve(a, b)

    # squaring and summing the opinion vector
    squared = np.square(solutions)

    summed = np.sum(squared)

    # result is normalized according to network size
    return summed / len(list(g.nodes))


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

    # se the new opinion values
    nx.set_node_attributes(g, attrs)

    return g


def brute_force_opposing_views(graph, pickle_name):
    """""
    This method brute forces all opposing opinion nodes and find the decrease of the network
    by adding every possible edge between them. (1 edge at a time). Also stores the resulting
    dictionary in a pickle file

    ##todo maybe implement 2,3,4,.. edge additions? too much time?

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


def main():
    # find_increase_in_graphs_with_addition()

    # options karate, polblogs
    name = 'karate'
    graph = load_graph(f'{name}.gml', True)

    decreasing_dictionary = brute_force_opposing_views(graph, f'{name}.pickle')

    check_properties(graph, decreasing_dictionary)

    print(get_polarization(graph))


if __name__ == "__main__":
    main()
