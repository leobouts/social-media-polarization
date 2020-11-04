import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def visualize_edge_removal(g, edge_list, title, img_name):
    """
    :param g:
    :param dictionary:
    :param title:
    :param img_name:
    :return:
    """

    tuples = []
    edge_colors = []
    edge_weights = []
    g = g.copy()

    # get all the node values
    node_values = nx.get_node_attributes(g, 'value')

    # store the values that will color the nodes
    # according to their polarity
    node_colors = []

    for polarization_value in node_values.values():
        if polarization_value > 0:
            node_colors.append('#00c08a')
        else:
            node_colors.append('#ffb74b')

    # create edges to add
    for i in range(len(edge_list)):
        edge_splitted = edge_list[i].split(",")
        tuples.append((int(edge_splitted[0]), int(edge_splitted[1])))

    g.add_edges_from(tuples)

    # keep same layout
    # pos = nx.spring_layout(g_top, scale=15)
    pos = nx.nx_agraph.graphviz_layout(g, prog='twopi')
    for edge in g.edges:
        if edge in tuples:
            edge_colors.append('#ff5255')
            edge_weights.append(2.5)
        else:
            edge_colors.append('black')
            edge_weights.append(0.7)

    # bigger nodes -> more central
    pr = nx.pagerank(g)
    nodes = nx.draw_networkx_nodes(g,
                                   pos,
                                   node_size=[11000 * v for v in pr.values()])
    nodes.set_edgecolor('black')
    nx.draw_networkx(g,
                     node_color=node_colors,
                     edge_color=edge_colors,
                     with_labels=True,
                     linewidths=1,
                     pos=pos,
                     node_size=[10000 * v for v in pr.values()],
                     width=edge_weights)
    plt.title(f'{title}')
    plt.savefig(f'{img_name}.png', dpi=800)
    plt.show()


def vis_graphs_heuristics(x_axis, y_axis_0, y_axis_1, y_axis_2, y_axis_3, label_0, label_1, label_2, label_3, title, x_label, y_label):

    plt.plot(x_axis, y_axis_0, label=label_0)
    plt.plot(x_axis, y_axis_1, label=label_1)
    plt.plot(x_axis, y_axis_2, label=label_2)
    plt.plot(x_axis, y_axis_3, label=label_3)

    # Add legend
    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    # Add title and x, y labels
    plt.title(title, fontsize=16, fontweight='bold')

    plt.xticks(x_axis)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig(f'{title}.eps', format='eps', dpi=1200)
    plt.show()
