from __compute_polarization__ import get_polarization
from __visualize__ import vis_graphs_heuristics
from numpy import linalg as linear_algebra
import networkx as nx
import pickle


def add_edges_and_count_polarization(edges_list, graph):
    """
    :param edges_list: a list of tuple edges [(1, 2), (2, 3), ...]
    :param graph: networkx graph
    :return: the polarization after adding these edges to the graph
    """

    g_copy = graph.copy()
    g_copy.add_edges_from(edges_list)
    pol, converged_opinions = get_polarization(g_copy)
    return pol


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


def open_pickles_for_adjusting_visualization_manually(k, dataset_name):
    with open(f"../pickles/{dataset_name}/{dataset_name}_decreases_checked_pol", 'rb') as fp:
        decreases_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{dataset_name}_labels_checked_pol", 'rb') as fp:
        labels_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{dataset_name}_times_checked", 'rb') as fp:
        times_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{dataset_name}_labels_checked_time", 'rb') as fp:
        time_labels_checked = pickle.load(fp)

    k_copy = k.copy()
    k_copy.insert(0, 0)

    vis_graphs_heuristics(k_copy,
                          decreases_checked,
                          labels_checked,
                          f"{dataset_name} Polarization Decrease",
                          "Number of Edges Added",
                          "π(z)",
                          0)

    vis_graphs_heuristics(k,
                          times_checked,
                          time_labels_checked,
                          f"{dataset_name} Time Elapsed",
                          "Number of Edges Added",
                          "Seconds",
                          1)


def open_info_pickle(dataset_name):
    with open(f"../pickles/{dataset_name}/{dataset_name}_info", 'rb') as fp:
        info = pickle.load(fp)

    return info


def format_edge_list_from_tuples(edge_list):
    return [f'{e[0]},{e[1]}' for e in edge_list]


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


def check_for_same_results(total_decreases, algorithms, mode):
    """
    This function merges all same polarization decreases in one, for example
    if two algorithms have the exact same decrease list then this will merge them
    and also merge its labels so it can be visualized correctly

    :param total_decreases: list of lists that contain polarization decreases
    :param algorithms: list of string labels
    :param mode: 0 for time graphs, 1 for polarization graphs
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

            check = 0

            if mode == 1:
                if total_decreases[i] == total_decreases[j]:
                    check = 1
            else:
                sum_1 = sum(total_decreases[i])
                sum_2 = sum(total_decreases[j])
                equal_range = 2
                if sum_1 + equal_range > sum_2 > sum_1 - equal_range:
                    check = 1

            if check:
                last_flag = False
                new_list_decreases = total_decreases.copy()
                new_list_decreases.remove(total_decreases[i])

                algorithms_new = algorithms.copy()
                new_label = algorithms[i] + " and " + algorithms[j]
                algorithms_new[j] = new_label

                algorithms_new.remove(algorithms[i])
                new_list_decreases, algorithms_new = check_for_same_results(new_list_decreases, algorithms_new, mode)

    if last_flag:
        return total_decreases, algorithms
    else:
        return new_list_decreases, algorithms_new


def get_positive_and_negative_values(nodeDict):
    positive_dictionary = {}
    negative_dictionary = {}

    for node in nodeDict:
        node_value = nodeDict[node]['value']
        if int(node_value) > 0:
            positive_dictionary[node] = node_value
        else:
            negative_dictionary[node] = node_value

    positive_dictionary = sorted(positive_dictionary.items(), key=lambda x: x[1], reverse=True)
    negative_dictionary = sorted(negative_dictionary.items(), key=lambda x: x[1], reverse=False)

    return positive_dictionary, negative_dictionary


def get_dataset_statistics(g):
    return nx.info(g)