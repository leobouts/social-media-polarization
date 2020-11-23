from __compute_polarization__ import get_polarization
from __helpers__ import add_edges_and_count_polarization, get_positive_and_negative_values
from node2vec import Node2Vec
from sklearn.linear_model import LogisticRegression

def greedy(k, graph_in):
    graph = graph_in.copy()
    k_items = []

    for i in range(k):
        edges, polarization = greedy_batch(k, graph)

        edge_1 = edges[0][0][0]
        edge_2 = edges[0][0][1]

        graph.add_edge(edge_1, edge_2)
        k_items.append((edge_1, edge_2))

    return k_items, get_polarization(graph)


def greedy_batch(k, graph_in):
    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    original_polarization = get_polarization(graph)
    addition_info = {}

    positive_dictionary, negative_dictionary = get_positive_and_negative_values(nodeDict)

    for i, node_pos in enumerate(positive_dictionary):
        for j, node_neg in enumerate(negative_dictionary):

            edge_to_add = (node_pos[0], node_neg[0])

            if graph.has_edge(*edge_to_add):
                continue

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])
            polarization_after_addition = get_polarization(g_copy)
            decrease = original_polarization - polarization_after_addition
            addition_info[edge_to_add] = decrease

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=True)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph)

    return k_items, polarization


def skip(k, graph_in):
    graph = graph_in.copy()

    nodeDict = dict(graph.nodes(data=True))
    positive_dictionary, negative_dictionary = get_positive_and_negative_values(nodeDict)

    first_pass_polarization = []

    first_of_negative = negative_dictionary[0][0]

    edges_to_add_list = []

    for positive_opinion in positive_dictionary:
        g_copy = graph.copy()
        g_copy.add_edges_from([(positive_opinion[0], first_of_negative)])
        polarization_after_addition = get_polarization(g_copy)

        first_pass_polarization.append(polarization_after_addition)

    for i, node_pos in enumerate(positive_dictionary):
        for j, node_neg in enumerate(negative_dictionary):

            edge_to_add = (node_pos[0], node_neg[0])

            if graph.has_edge(*edge_to_add):
                continue

            if i == len(positive_dictionary):
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])
            polarization_after_addition = get_polarization(g_copy)

            if first_pass_polarization[i + 1] < polarization_after_addition:
                break

            edges_to_add_list.append(edge_to_add)
            if len(edges_to_add_list) == k:
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization


def distance(k, graph_in):
    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    positive_dictionary, negative_dictionary = get_positive_and_negative_values(nodeDict)

    edges_to_add_list = []

    for i, node_pos in enumerate(positive_dictionary):
        node_pos_value = node_pos[1]

        for j, node_neg in enumerate(negative_dictionary):

            node_neg_value = node_neg[1]
            edge_to_add = (node_pos[0], node_neg[0])

            if graph.has_edge(*edge_to_add):
                continue

            if i == len(positive_dictionary):
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])

            distance_current = abs(node_pos_value - node_neg_value)
            distance_to_check = abs(positive_dictionary[i + 1][1] - node_neg_value)

            if distance_to_check > distance_current:
                break

            edges_to_add_list.append(edge_to_add)
            if len(edges_to_add_list) == k:
                polarization = add_edges_and_count_polarization(edges_to_add_list, graph)
                return edges_to_add_list, polarization


def expressed(k, graph_in, mode):
    """
    :param k:
    :param graph_in:
    :param mode: 1 for distance, 2 for multiplication
    :return:
    """
    graph = graph_in.copy()
    nodeDict = dict(graph.nodes(data=True))
    addition_info = {}

    positive_dictionary, negative_dictionary = get_positive_and_negative_values(nodeDict)

    for i, node_pos in enumerate(positive_dictionary):
        for j, node_neg in enumerate(negative_dictionary):

            edge_to_add = (node_pos[0], node_neg[0])

            if graph.has_edge(*edge_to_add):
                continue

            g_copy = graph.copy()
            g_copy.add_edges_from([edge_to_add])
            node_1 = nodeDict[node_pos[0]]['value']
            node_2 = nodeDict[node_neg[0]]['value']

            if mode == 1:
                val = abs(node_1 - node_2)
            else:
                val = node_1 * node_2

            addition_info[edge_to_add] = val

            if mode == 1:
                flag = True
            else:
                flag = False

    sorted_edges = sorted(addition_info.items(), key=lambda x: x[1], reverse=flag)

    k_items = sorted_edges[:k]

    edges_to_add_list = [edge[0] for edge in k_items]
    polarization = add_edges_and_count_polarization(edges_to_add_list, graph)

    return k_items, polarization


def graph_embeddings(g, name):

    n2v_obj = Node2Vec(g, dimensions=10, walk_length=5, num_walks=10, p=1, q=1, workers=1)
    model = n2v_obj.fit(min_count=2, window=3)

    # Save embeddings for later use
    model.wv.save_word2vec_format(f'../node2vec_models/titles_{name}.emb')

    # Look for most similar nodes
    #model.wv.most_similar('2')  # Output node names are always strings



