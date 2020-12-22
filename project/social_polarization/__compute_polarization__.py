import time

from scipy.sparse import identity
import networkx as nx
import numpy as np
from numpy.linalg import norm
from tqdm import trange


def get_polarization(g):
    """"
    Creates the L+I matrix that is holded in variable f where L is the laplacian matrix of the graph.
    solves the (L+I)^-1 * S system and computes the polarization index value from the second norm of this
    array squared and normalized.

    --------------------------------------------------------------------------------------------------
    :param g: networkx graph with value attributes
    :return: Value of the polarization index
    """

    start = time.time()

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
    end = time.time()

    print("time:", end - start)

    # result is normalized according to network size
    return summed / no_of_nodes


def friedkinJohnsen(g):

    start = time.time()
    N = len(g.nodes)

    s = list(nx.get_node_attributes(g, 'value').values())

    new_opinions = [0] * N

    convergence = 1

    while 1:

        for i in range(len(new_opinions)):

            sum_z = new_opinions[i]
            neighbors = list(g.neighbors(i + 1))

            for neighbor in neighbors:
                sum_z += new_opinions[neighbor - 1]

            new_opinions[i] = (s[i] + sum_z) / (1 + len(neighbors) + 1)

        # squaring and summing the opinion vector
        squared = np.square(new_opinions)

        summed = np.sum(squared)

        if abs(convergence - (summed / N)) < 0.001:
            break

        convergence = summed / N
    end = time.time()

    print("time:", end - start)
    # result is normalized according to network size
    return summed / N
