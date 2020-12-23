from scipy.sparse import identity
import networkx as nx
import numpy as np
from numpy.linalg import norm


def get_polarization_with_inverse(g):
    """"
    Creates the L+I matrix that is holded in variable f where L is the laplacian matrix of the graph.
    solves the (L+I)^-1 * S system and computes the polarization index value from the second norm of this
    array squared and normalized.

    --------------------------------------------------------------------------------------------------
    :param g: networkx graph with value attributes
    :return: Value of the polarization index
    """

    no_of_nodes = len(g.nodes)

    values = list(nx.get_node_attributes(g, 'value').values())

    Laplace = nx.laplacian_matrix(g)
    Identity = identity(no_of_nodes)
    L_plus_I = Laplace + Identity

    Inverse = np.linalg.inv(L_plus_I.todense())

    # computing (L+I)^-1 * S
    solutions = Inverse.dot(values)

    # squaring and summing the opinion vector
    squared = np.square(solutions)

    summed = np.sum(squared)

    # result is normalized according to network size
    return summed / no_of_nodes


def get_polarization(g):
    '''

    :param g:
    :return:
    '''

    N = len(g.nodes)

    s = list(nx.get_node_attributes(g, 'value').values())

    new_opinions = [0] * N

    convergence = 1

    while 1:

        for i in range(len(new_opinions)):

            sum_z = new_opinions[i]

            neighbors = list(g.neighbors(i))

            for neighbor in neighbors:
                sum_z += new_opinions[neighbor]

            # derived from the friedkin johnson formula, assuming weights are 1 and neighbors includes self.
            new_opinions[i] = (int(s[i]) + sum_z) / (1 + len(neighbors) + 1)

        # squaring and summing the opinion vector
        squared = np.square(new_opinions)

        summed = np.sum(squared)

        # adjust here the accuracy
        if abs(convergence - (summed / N)) < 0.0001:
            break

        convergence = summed / N

    # result is normalized according to network size
    return summed / N, new_opinions
