import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import copy


def visualize_graph(g, top_decrease, small_decrease):

    top_tuples = []
    small_tuples = []

    g_top = g.copy()
    g_small = g.copy()

    # get all the node values
    node_values = nx.get_node_attributes(g_top, 'value')

    # store the values that will color the nodes
    # according to their polarity
    node_colors = []

    for polarization_value in node_values.values():
        if polarization_value > 0:
            node_colors.append('#f11712')
        else:
            node_colors.append('#0099f7')

    # create edges to add
    for i in range(len(top_decrease)):
        edge_splitted = top_decrease[i].split(",")
        top_tuples.append((int(edge_splitted[0]), int(edge_splitted[1])))

        edge_splitted = small_decrease[i].split(",")
        small_tuples.append((int(edge_splitted[0]), int(edge_splitted[1])))

    g_top.add_edges_from(top_tuples)
    g_small.add_edges_from(small_tuples)

    edge_colors_top = []
    edge_colors_small = []

    # keep same layout
    #pos = nx.spring_layout(g_top, scale=15)
    pos = nx.nx_agraph.graphviz_layout(g_top, prog='twopi')
    for edge in g_top.edges:
        if edge in top_tuples:
            edge_colors_top.append('#ffe63a')
        else:
            edge_colors_top.append('black')

    for edge in g_small.edges:
        if edge in small_tuples:
            edge_colors_small.append('#ffe63a')
        else:
            edge_colors_small.append('black')

    # bigger nodes -> more central
    pr = nx.pagerank(g_top)
    nodes = nx.draw_networkx_nodes(g_top,
                                   pos,
                                   node_size=[11000*v for v in pr.values()])
    nodes.set_edgecolor('black')
    nx.draw_networkx(g_top,
                     node_color=node_colors,
                     edge_color=edge_colors_top,
                     with_labels=True,
                     linewidths=1,
                     pos=pos,
                     node_size=[10000*v for v in pr.values()])
    plt.title('Largest decrease additions')
    plt.savefig('largest.png', dpi=1200)
    plt.show()

    pr = nx.pagerank(g_small)
    nodes = nx.draw_networkx_nodes(g_small,
                                   pos,
                                   node_size=[11000 * v for v in pr.values()])
    nodes.set_edgecolor('black')
    nx.draw_networkx(g_small,
                     node_color=node_colors,
                     edge_color=edge_colors_small,
                     with_labels=True,
                     linewidths=1,
                     pos=pos,
                     node_size=[10000*v for v in pr.values()])
    plt.title('Smallest decrease additions')
    plt.savefig('smallest.png', dpi=1200)
    plt.show()


