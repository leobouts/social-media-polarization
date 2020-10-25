import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def visualize_graph(g, top_decrease, small_decrease, operation):
    '''
    :param g:
    :param top_decrease:
    :param small_decrease:
    :param operation: 'removal' or 'addition'
    :return:
    '''

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
            node_colors.append('#00c08a')
        else:
            node_colors.append('#ffb74b')

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

    edge_weights_top = []
    edge_weights_small = []

    # keep same layout
    # pos = nx.spring_layout(g_top, scale=15)
    pos = nx.nx_agraph.graphviz_layout(g_top, prog='twopi')
    for edge in g_top.edges:
        if edge in top_tuples:
            edge_colors_top.append('#ff5255')
            edge_weights_top.append(2.5)
        else:
            edge_colors_top.append('black')
            edge_weights_top.append(0.7)

    for edge in g_small.edges:
        if edge in small_tuples:
            edge_colors_small.append('#ff5255')
            edge_weights_small.append(2.5)
        else:
            edge_colors_small.append('black')
            edge_weights_small.append(0.7)

    # bigger nodes -> more central
    pr = nx.pagerank(g_top)
    nodes = nx.draw_networkx_nodes(g_top,
                                   pos,
                                   node_size=[11000 * v for v in pr.values()])
    nodes.set_edgecolor('black')
    nx.draw_networkx(g_top,
                     node_color=node_colors,
                     edge_color=edge_colors_top,
                     with_labels=True,
                     linewidths=1,
                     pos=pos,
                     node_size=[10000 * v for v in pr.values()],
                     width=edge_weights_top)
    plt.title(f'Largest decrease {operation}')
    plt.savefig('largest.png', dpi=800)
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
                     node_size=[10000 * v for v in pr.values()],
                     width=edge_weights_small)
    plt.title(f'Smallest decrease {operation}')
    plt.savefig('smallest.png', dpi=800)
    plt.show()


def vis_graphs_heuristics(x_axis, y_axis_1, y_axis_2, y_axis_3, label_1, label_2, label_3, title, x_label, y_label):

    plt.plot(x_axis, y_axis_1, label=label_1)
    plt.plot(x_axis, y_axis_2, label=label_2)
    plt.plot(x_axis, y_axis_3, label=label_3)

    # Add legend
    plt.legend(loc='lower left')

    # Add title and x, y labels
    plt.title(title, fontsize=16, fontweight='bold')

    plt.xticks(x_axis)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
