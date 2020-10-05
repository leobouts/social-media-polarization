import pickle
import pprint

with open('polblogs_edges.pickle', 'rb') as fp:
    edge_dictionary = pickle.load(fp)
    pprint.pprint(sorted(edge_dictionary))
