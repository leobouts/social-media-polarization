import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

alphaVal = 0.8
linethick = 3.5


def get_dash_markers_colors(i):
    if i == 'Greedy':
        return [3, 1], 8, 'green'
    elif i == 'GBatch':
        return [1000, 1], "^", '#ff6961'
    elif i == 'FTGreedy':
        return [2, 1, 10, 1], 9, 'blue'
    elif i == 'FTGreedyBatch':
        return [4, 1, 1, 1, 1, 1], 8, 'black'
    elif i == 'Expressed Distance' or i == 'BExpressed Distance':
        return [3, 1], 10, 'red'
    elif i == 'Random different':
        return [1000, 1], 'None', 'orange'
    elif i == 'Random':
        return [1000, 1], 'None', 'pink'
    else:
        return [1000, 1], 'None', 'pink'



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

    # x_axis = [str(x) for x in x_axis]
    print(list_of_labels)
    for i, y_axis in enumerate(list_of_axes):

        dash, marker, color = get_dash_markers_colors(list_of_labels[i])

        plt.plot(x_axis,
                 y_axis,
                 color=color,
                 linestyle='-',
                 dashes=dash,
                 marker=marker,
                 label=list_of_labels[i],
                 alpha=alphaVal,
                 markersize=10)

    # Add legend
    # Put a legend below current axis

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, shadow=True, ncol=5)

    # Add title and x, y labels
    plt.title(title, fontsize=16, fontweight='bold')

    # rounding and y ticks
    # flat_list = [item for sublist in list_of_axes for item in sublist]
    #
    # multiplier = 10 ** 3
    # val = min(flat_list * multiplier) / multiplier
    #
    # tick1 = np.arange(val, list_of_axes[0][0]+0.03, 0.02)
    # plt.yticks(tick1)

    plt.xticks(x_axis)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig(f'../figures_generated/{title.split(" ")[0]}/{title}.pdf', dpi=100, bbox_inches='tight')
    plt.show()


def vis_graphs_heuristics_bar(x_axis, list_of_axes, list_of_labels, title, x_label, y_label, mode):
    # fig, is the whole thing; ax1 is a subplot in the figure,
    # so we reference it to plot bars and lines there
    fig, ax1 = plt.subplots()

    ind = np.arange(len(x_axis))
    width = 0.10

    xticklabels = x_axis

    flat_list = [item for sublist in list_of_axes for item in sublist]
    minimum_value = min(flat_list)
    maximum_value = max(flat_list)

    all_groups = list_of_axes

    # plot each group of bars; loop-variable bar_values contains values for bars
    for i, bar_values in enumerate(all_groups):
        # compute position for each bar
        bar_position = width * i

        ax1.bar(ind + bar_position, bar_values, width, alpha=alphaVal, color=get_color(list_of_labels[i]))

    # plot line for each group of bars; loop-variable y_values contains values for lines
    for i, y_values in enumerate(all_groups):
        # moves the beginning of a line to the middle of the bar
        additional_space = (width * i) + (width / 2)
        # x_values contains list indices plus additional space
        x_values = [x + additional_space for x, _ in enumerate(y_values)]

        # simply plot the values in y_values
        ax1.plot(x_values, y_values, alpha=alphaVal, lw=2.1, color=get_color(list_of_labels[i]))

    # sets the minimum value of the bar to the lowest value plus a small number
    # useful for experiments in big datasets and small edge additions that
    # don't reduce the polarization a lot
    # adjust for each dataset by hand

    #karate books
    #set_min = minimum_value-0.02
    #set_max = maximum_value + 0.03

    set_min = minimum_value-0.002
    set_max = maximum_value + 0.003

    ax1.set(ylim=[set_min, set_max])

    plt.title(title, fontsize=16, fontweight='bold')
    plt.setp([ax1], xticks=ind + width, xticklabels=xticklabels)

    plt.legend(list_of_labels, loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, shadow=True, ncol=3)

    plt.tight_layout()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(f'../figures_generated/{title.split(" ")[0]}/{title}.pdf', dpi=100, bbox_inches='tight')
    plt.show()


def final_plot(df, dataset_names, k, labels_checked):
    greedy_c = '#329932'
    gbatc_c = '#e31a1c'
    ftgreedy_c = '#BB0099'
    ftgreedyb_c = '#fdbf6f'
    expr_dis_c = '#2166ac'
    expr_mul_c = '#6a3d9a'
    random_c = '#b2182b'

    # num_of_edges = [
    #     [0, 10, 20, 30, 40],
    #     [0, 25, 50, 75, 100],
    #     [0, 200, 400, 600, 800],
    #     [0, 400, 800, 1200, 1600],
    #     [0, 700, 1400, 2100, 2800],
    #     [0, 500, 1000, 1500, 2000],
    # ]

    fig2, axes = plt.subplots(nrows=2, ncols=3)

    for i, ax in enumerate(axes.flatten()):

        # attention!!!11111 adjust these also, leave only the appropriate for every dataset for every experiment

        if dataset_names[i] == 'beefban':
            colors = [ftgreedy_c, ftgreedyb_c, expr_dis_c, expr_mul_c, random_c]

        elif dataset_names[i] == 'karate' or dataset_names[i] == 'books':
            colors = [greedy_c, gbatc_c, ftgreedy_c, ftgreedyb_c, expr_dis_c, expr_mul_c, random_c]

        else:
            colors = [ftgreedy_c, ftgreedyb_c, expr_dis_c, expr_mul_c, random_c]

        # if dataset_names[i] == 'karate' or dataset_names[i] == 'books':
        #     colors = [greedy_c, gbatc_c, ftgreedy_c, ftgreedyb_c, expr_dis_c, expr_mul_c, random_c]
        #
        # else:
        #     colors = [expr_dis_c, expr_mul_c, random_c]

        df[i].T.plot(color=colors,
                     linestyle='-',
                     dashes=[2, 1, 10, 1],
                     lw=linethick,
                     title=dataset_names[i],
                     alpha=alphaVal,
                     legend=False,
                     ax=ax)

        # if u need different edges in the plots just do it by hand, eitherway it doesnt matter so much
        # for the same use the variable k

        # ax.set_xticks(num_of_edges[i], minor=False)

        ax.set_xticks(k, minor=False)

    fig2.legend(labels_checked, bbox_to_anchor=(1, -0.05), fancybox=True, shadow=True, ncol=4)
    fig2.text(0.5, 0, 'Number of edges added', ha='center', va='center')
    fig2.text(0, 0.5, 'E[π(z)]', ha='center', va='center', rotation='vertical')
    fig2.tight_layout()
    plt.savefig(f'../figures_generated/final/final.pdf', dpi=300, bbox_inches='tight')

    plt.show()
