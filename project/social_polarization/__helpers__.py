from __compute_polarization__ import get_polarization
from numpy import linalg as linear_algebra
import networkx as nx
import pickle
import pprint


def add_edges_and_count_polarization(edges_list, graph):
    """
    :param edges_list: a list of tuple edges [(1, 2), (2, 3), ...]
    :param graph: networkx graph
    :return: the polarization after adding these edges to the graph
    """

    g_copy = graph.copy()
    g_copy.add_edges_from(edges_list)

    return get_polarization(g_copy)


def make_graph_fully_connected(g):
    """
    :param g: networkx graph
    :return: fully connected graph g, also prints information of the graph
    before and after making it fully connected
    """

    print(nx.info(g))

    edges_to_be_added = list(nx.non_edges(g))
    g.add_edges_from(edges_to_be_added)

    print(nx.info(g))

    return g


def open_pickles(pickle_name):
    """
    :param pickle_name: name of the pickle file that is gonna be oppened
    :return: nothing, prints the state of the pickle file.
    """

    with open(pickle_name, 'rb') as fp:
        edge_dictionary = pickle.load(fp)
        pprint.pprint(sorted(edge_dictionary))


def format_edge_list(dict_to_format):
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


def convert_dataset_to_gml(node_values_path, edges_path, name_to_save):
    f = open(node_values_path, "r")
    label_list = []
    value_list = []
    tuples_list = []

    for x in f:
        splitted = x.rstrip().split(",")
        label_list.append(splitted[0])
        value_list.append(splitted[1])

    f = open(edges_path, "r")

    if "ClintonTrump" not in name_to_save:
        for x in f:
            splitted = x.rstrip().split(",")
            edge_1 = splitted[0]
            edge_2 = splitted[1]
            tuples_list.append((edge_1, edge_2))
    else:
        for x in f:
            splitted = x.rstrip().split(" ")
            edge_1 = splitted[0]
            edge_2 = splitted[1]
            tuples_list.append((edge_1, edge_2))

    with open(f'../datasets/{name_to_save}', 'w') as the_file:

        the_file.write('graph\n')
        the_file.write('[\n')

        if "ClintonTrump" in name_to_save:
            the_file.write('  directed 0\n')

        for i, node in enumerate(label_list):

            the_file.write('  node\n')
            the_file.write('  [\n')
            the_file.write(f'    id {i}\n')
            the_file.write(f'    label "{node}"\n')
            if "ClintonTrump" in name_to_save:
                the_file.write(f'    value "{value_list[i]}"\n')
            else:
                the_file.write(f'    value {value_list[i]}\n')
            the_file.write('  ]\n')

        for edge in tuples_list:
            the_file.write('  edge\n')
            the_file.write('  [\n')
            the_file.write(f'    source {label_list.index(edge[0])}\n')
            the_file.write(f'    target {label_list.index(edge[1])}\n')
            the_file.write('  ]\n')
        the_file.write(']\n')


def conservative_liberal_conversion(g):
    value_dictionary = nx.get_node_attributes(g, 'value')

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

    nx.set_node_attributes(g, attrs)

    return g


def zero_value_conversion(g):
    # get the values of the new graph in a dictionary
    value_dictionary = nx.get_node_attributes(g, 'value')

    # opinions vary from 0 to 1, find all zero occurences
    zero_indices = [k for (k, v) in value_dictionary.items() if v == 0]

    # empty dictionary
    attrs = {}

    # create the dictionary that will update 0 nodes to -1
    for obj in zero_indices:
        d = {obj: {'value': -1}}
        attrs.update(d)

    # se the new opinion values
    nx.set_node_attributes(g, attrs)

    return g


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
    print(linear_algebra.norm(closeness_c))
    print("============================")
    print("Betweeness centrality:")
    print(betweenness_c)
    print("Norm:")
    print(linear_algebra.norm(betweenness_c))
    print("============================")
    print("Eigen centrality:")
    print(eigen_c)
    print("Norm:")
    print(linear_algebra.norm(eigen_c))


def check_for_same_results(total_decreases, algorithms):
    """
    This function merges all same polarization decreases in one, for example
    if two algorithms have the exact same decrease list then this will merge them
    and also merge its labels so it can be visualized correctly

    :param total_decreases: list of lists that contain polarization decreases
    :param algorithms: list of string labels
    :return: merged list for visualisation and labels
    """

    if range(len(algorithms) == 1):
        return total_decreases, algorithms

    new_list_decreases = []
    algorithms_new = []
    last_flag = True

    for i in range(len(algorithms)):
        for j in range(i, len(algorithms)):
            if i == j:
                continue
            if total_decreases[i] == total_decreases[j]:
                last_flag = False
                new_list_decreases = total_decreases.copy()
                new_list_decreases.remove(total_decreases[i])

                algorithms_new = algorithms.copy()
                new_label = algorithms[i] + " and " + algorithms[j]
                algorithms_new[j] = new_label

                algorithms_new.remove(algorithms[i])
                new_list_decreases, algorithms_new = check_for_same_results(new_list_decreases, algorithms_new)

    if last_flag:
        return total_decreases, algorithms
    else:
        return new_list_decreases, algorithms_new


def get_positive_and_negative_values(nodeDict):

    positive_dictionary = {}
    negative_dictionary = {}

    for node in nodeDict:
        node_value = nodeDict[node]['value']
        if node_value > 0:
            positive_dictionary[node] = node_value
        else:
            negative_dictionary[node] = node_value

    positive_dictionary = sorted(positive_dictionary.items(), key=lambda x: x[1], reverse=True)
    negative_dictionary = sorted(negative_dictionary.items(), key=lambda x: x[1], reverse=True)

    return positive_dictionary, negative_dictionary