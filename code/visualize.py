import matplotlib.pyplot as plt
import networkx as nx


def visualize_graph(g, top_decrease, small_decrease):
    top_tuples = []
    small_tuples = []

    # create edges to add
    for i in range(len(top_decrease)):
        edge_splitted = top_decrease[i].split(",")
        top_tuples.append((int(edge_splitted[0]), int(edge_splitted[1])))

        edge_splitted = small_decrease[i].split(",")
        small_tuples.append((int(edge_splitted[0]), int(edge_splitted[1])))

    g.add_edges_from(top_tuples)
    g.add_edges_from(small_tuples)

    edge_colors = []

    for edge in g.edges:
        if edge in top_tuples:
            edge_colors.append('green')
        elif edge in small_tuples:
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    nx.draw_spring(g, edge_color=edge_colors, with_labels=True)

    plt.title('The karate network')
    plt.show()
