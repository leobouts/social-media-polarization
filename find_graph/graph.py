from graph_topologies import *
import itertools
import numpy as np


def check_graph_permutations(number_of_vertices, graph):

    # make a list of nodes e.g. for 3 nodes returns [1,2,3]
    lst_nodes = [node for node in range(number_of_vertices)]

    # get all possible permutations for the values
    value_permutations = [list(i) for i in itertools.product([-1, 1], repeat=number_of_vertices)]

    edge_permutations = [i for i in itertools.combinations(lst_nodes, 2)]

    # creates all possible pairs, pairs of two, of three etc.. up to number of vertices-1
    possible_combs = [i for i in itertools.combinations(edge_permutations, number_of_vertices-1)]

    # wrap the edges addition in a tuple for compatibility issues bellow
    additions_tuple = list(zip(edge_permutations))

    # join all the possible edge additions in one list
    possible_combs.extend(additions_tuple)

    # check all value and edge combinations

    for perm in value_permutations:

        initial_polarization = get_polarization(graph, perm)

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

                new_pol = get_polarization(g, perm)

                if new_pol > initial_polarization:
                    # print(nx.info(graph))
                    # print(nx.info(g))
                    print("===================")
                    print("graph topology:", graph.name)
                    print("values", perm)
                    print("initial:", initial_polarization)
                    print("after:", new_pol)
                    print("addition", edge_additions)
                    print("==============")


# solves a system of linear equations that are taken from the graph topology
# then computes the polarization.

def get_polarization(g, values):

    equations = []

    nodes = list(g.nodes)
    nodes = sorted(nodes)

    for node in nodes:

        neighbors = [n for n in g.neighbors(node)]
        neighbors = sorted(neighbors)

        f = [-1 if a in neighbors else 0 for a in nodes]

        f[node] = len(neighbors) + 1

        equations.append(f)

    a = np.array(equations)
    b = np.array(values)

    solutions = np.linalg.solve(a, b)

    squared = np.square(solutions)

    summed = np.sum(squared)

    rooted = np.sqrt(summed)

    return rooted / len(list(g.nodes))


def main():

    for g_type in get_all_graphs():

        graph = get_graph_type(g_type)

        topology = graph[0]
        size = graph[1]

        check_graph_permutations(size, topology)


if __name__ == "__main__":
    main()


