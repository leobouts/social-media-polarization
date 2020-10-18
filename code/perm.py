import random

from tqdm import tqdm

from graph_topologies import *
from graph import get_polarization, attach_values_from_list_to_graph
import itertools


def check_graph_permutations(number_of_vertices, graph):

    # make a list of nodes e.g. for 3 nodes returns [1,2,3]
    lst_nodes = [node for node in range(number_of_vertices)]

    # get all possible permutations for the values
    value_permutations = []
    for i in itertools.product([-0.8, -0.5, 0.1, 0, -0.9, 0.8, -0.1, 0.5], repeat=number_of_vertices):
        value_permutations.append(list(i))

    edge_permutations = [i for i in itertools.combinations(lst_nodes, 2)]

    # creates all possible pairs, pairs of two, of three etc.. up to number of vertices-1
    possible_combs = [i for i in itertools.combinations(edge_permutations, number_of_vertices-1)]

    # wrap the edges addition in a tuple for compatibility issues bellow
    additions_tuple = list(zip(edge_permutations))

    # join all the possible edge additions in one list
    possible_combs.extend(additions_tuple)

    # check all value and edge combinations

    decrease = {}

    for perm in value_permutations:

        initial_polarization = get_polarization(graph)

        for edge_additions in possible_combs:

            # re-init graph to check different edge scenario
            g = nx.Graph()
            g.add_edges_from(graph.edges())

            # check if the addition already exist in the graph, every addition must NOT be
            # an edge that exists inside the graph beforehand.
            # exist = True : all edge_additions does not exist in the current graph
            # exist = False: at least one edge addition in edge_additions exist in the current graph

            exist = all(x not in graph.edges() for x in edge_additions)

            # check that all the connections are with different opinions

            all_connections_different_opinions = all(perm[y[0]] * perm[y[1]] < 0 for y in edge_additions)

            if exist and all_connections_different_opinions:

                for edge_perm in edge_additions:
                    g.add_edge(edge_perm[0], edge_perm[1])

                new_pol = get_polarization(g)

                decrease[abs(initial_polarization-new_pol)] = {'graph': graph.name, 'values': perm,
                                                          'edge_additions': edge_additions}

                if new_pol > initial_polarization:
                    print(nx.info(graph))
                    print(nx.info(g))
                    print("===================")
                    print("graph topology:", graph.name)
                    print("values", perm)
                    print("initial:", initial_polarization)
                    print("after:", new_pol)
                    print("addition", edge_additions)
                    print("==============")

    print(max(decrease))
    print(decrease[max(decrease)])


def find_increase_in_graphs_with_addition():

    """
    finds if a graph has increased polarization after adding an edge
    between different opinions. the functions takes all the topologies
    that are specified in the graph_topologies.py file
    --------------------------------------------------------------------

    :returns: nothing, prints all graphs that have increased polarization
    """

    for g_type in get_all_graphs():

        graph = get_graph_type(g_type)

        topology = graph[0]
        size = graph[1]

        check_graph_permutations(size, topology)


def example_increase_that_confirms_intuition():

    graph, size = get_graph_type('intuition_graph')
    nodeDict = dict(graph.nodes(data=True))
    opinion_list = []

    list_negative = [comb for comb in itertools.combinations([-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1], 4)]
    print(len(list_negative))
    print(list_negative)
    list_positive = [comb for comb in itertools.permutations([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1], 3)]
    print(len(list_positive))
    print(list_positive)

    c = list(itertools.product(list_negative, list_positive))
    opinion_list = [list(itertools.chain(*items)) for items in c]
    print(len(opinion_list))
    print(opinion_list)
    print("ddd")

    for opinions in tqdm(opinion_list):

        graph = attach_values_from_list_to_graph(graph, opinions)

        edges_to_add = nx.non_edges(graph)
        original_polarization = get_polarization(graph)

        for edge in edges_to_add:

            node_a_val = nodeDict[edge[0]]['value']
            node_b_val = nodeDict[edge[1]]['value']
            g_copy = graph.copy()

            diff = abs(node_a_val - node_b_val)
            mul = node_a_val * node_b_val

            if 1.2 >= diff >= 0.8 and mul < 0:
                g_copy.add_edges_from([edge])
                polarization_after_addition = get_polarization(g_copy)

                if polarization_after_addition > original_polarization:
                    print("found one:")
                    print(edge)
                    print(nx.info(g_copy))
                    print(opinion_list)
                    return


def force_example(graph):

    nodeDict = dict(graph.nodes(data=True))
    edges_to_add = nx.non_edges(graph)
    original_polarization = get_polarization(graph)

    for edge in edges_to_add:

        node_a_val = nodeDict[edge[0]]['value']
        node_b_val = nodeDict[edge[1]]['value']
        g_copy = graph.copy()

        diff = abs(node_a_val - node_b_val)
        mul = node_a_val * node_b_val

        if 1.5 >= diff >= 0.8 and mul < 0:
            g_copy.add_edges_from([edge])
            polarization_after_addition = get_polarization(g_copy)

            if polarization_after_addition > original_polarization:
                print("found one:")
                print(edge)
                print(nx.info(g_copy))
