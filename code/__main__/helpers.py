from compute_polarization import get_polarization
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
