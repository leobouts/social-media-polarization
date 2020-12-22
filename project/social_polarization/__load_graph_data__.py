from __helpers__ import *
from perm import *


def load_graph(gml_file):
    """"
    Loads the graph from the gml_file that also have the values of expressed opinions. If these values
    are in the [0,1] the function can change them to [-1,1] by turning the zeros into negatives.
    If the values are ["c", "l', "n'], conservative, liberal or neutral the function changes them into -1, 0, 1
    accordingly.

    If we wan to add a new dataset that has [0,1] or ["c", "l', "n'] values we need to specify that it
    will be changed in the lists bellow.

    We also make sure we convert the graph to a simple one if the data contain multiple same edges
    (multigraph). Also multigraph data must have the flag "multigraph 1" in the header to work.

    :param gml_file: name of the stored values
    :return: networkx graph
    """

    name = gml_file.split("/")[2].split(".")[0]

    graph = nx.read_gml(gml_file, label='id')

    graph = nx.Graph(graph, name=name)

    conservative_liberal_convert = ['../datasets/books.gml',
                                    '../datasets/ClintonTrump.gml']

    zero_value_convert = ["../datasets/GermanWings.gml",
                          "../datasets/beefban.gml",
                          "../datasets/sxsw.gml",
                          "../datasets/karate.gml",
                          "../datasets/polblogs.gml"
                          ]

    if gml_file in conservative_liberal_convert:
        graph = conservative_liberal_conversion(graph)

    if gml_file in zero_value_convert:
        graph = zero_value_conversion(graph)

    # value_dictionary = nx.get_node_attributes(graph, 'value')
    #
    # list_of_graph_values = list(value_dictionary.values())
    #
    # graph = attach_values_from_list_to_graph(graph, list_of_graph_values)

    # print(list(graph.nodes(data=True)))
    # print(nx.info(graph))

    return graph

