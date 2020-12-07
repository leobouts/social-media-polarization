import time
import numpy as np
import networkx as nx
from scipy import sparse
from scipy.sparse import identity
from scipy.sparse.linalg import inv


def get_polarization(g):
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
