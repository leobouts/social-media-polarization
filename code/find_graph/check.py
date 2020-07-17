from graph import *

values = [-1, 1, -1, -1, 1]

test = nx.Graph()
test.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])

print(get_polarization(test, values))


test1 = nx.Graph()
test1.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)])

print(get_polarization(test1, values))
