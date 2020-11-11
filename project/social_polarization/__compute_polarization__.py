import numpy as np
import networkx as nx


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

