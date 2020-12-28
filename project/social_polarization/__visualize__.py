import matplotlib.pyplot as plt
import networkx as nx


def visualize_edge(g, edge_list, title, img_name, dataset, mode):
    """
    :param dataset:
    :param g: networkx graph
    :param edge_list: edges that are removed or added
    :param title: title we want the graph to have
    :param img_name: name of the image to be saved
    :param mode: 0 = removal, 1 = addition
    :return: visualization of addition/removal of edges
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
            node_colors.append('#f6d55c')
        else:
            node_colors.append('#20639b')

    # create edges as a tuple
    for i in range(len(edge_list)):
        edge_splitted = edge_list[i].split(",")
        tuples.append((int(edge_splitted[0]), int(edge_splitted[1])))

    tuples = [tuple(sorted(tup)) for tup in tuples]
    g.add_edges_from(tuples)

    # keep same layout
    # pos = nx.spring_layout(g_top, scale=15)
    pos = nx.nx_agraph.graphviz_layout(g, prog='twopi')

    for edge in g.edges:
        if edge in tuples:
            if mode:
                edge_colors.append('#339E66FF')
            else:
                edge_colors.append('#D01C1FFF')
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
    plt.savefig(f'../figures_generated/{dataset}/{img_name}.pdf', dpi=100)
    plt.show()


def vis_graphs_heuristics(x_axis, list_of_axes, list_of_labels, title, x_label, y_label, mode):

    for i, y_axis in enumerate(list_of_axes):

        if list_of_labels[i] == 'Greedy':
            color = '#d02324'
            ls = None

        elif list_of_labels[i] == 'GBatch':
            color = '#289628'
            ls = None

        elif list_of_labels[i] == 'FTGreedy':
            color = '#ff7410'
            ls = None

        elif list_of_labels[i] == 'Random':
            color = '#895cb5'
            ls = None

        elif list_of_labels[i] == 'FTGreedyBatch':
            color = '#d02324'
            ls = '-'

        elif list_of_labels[i] == 'Expressed Distance':
            color = '#289628'
            ls = '--'

        elif list_of_labels[i] == 'Expressed Multiplication':
            color = '#ff7410'
            ls = '-.'

        else:
            color = '#895cb5'
            ls = ':'

        plt.plot(x_axis, y_axis, label=list_of_labels[i], color=color, linestyle=ls)

    # Add legend
    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, shadow=True, ncol=5)

    # Add title and x, y labels
    plt.title(title, fontsize=16, fontweight='bold')

    plt.xticks(x_axis)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig(f'../figures_generated/{title.split(" ")[0]}/{title}.pdf', dpi=100, bbox_inches='tight')
    plt.show()
