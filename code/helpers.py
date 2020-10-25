from compute_polarization import get_polarization
import networkx as nx
import pickle
import pprint


def add_edges_and_count_polarization(edges_list, graph):

    g_copy = graph.copy()
    g_copy.add_edges_from(edges_list)

    return get_polarization(g_copy)


def make_graph_fully_connected(g):

    print(nx.info(g))

    edges_to_be_added = list(nx.non_edges(g))
    g.add_edges_from(edges_to_be_added)

    print(nx.info(g))

    return g


def open_pickles(pickle_name):

    with open(pickle_name, 'rb') as fp:
        edge_dictionary = pickle.load(fp)
        pprint.pprint(sorted(edge_dictionary))
