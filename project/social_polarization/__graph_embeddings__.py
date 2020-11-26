import pandas as pd
import numpy as np
import random
import networkx as nx
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from node2vec import Node2Vec

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


def load_embeddings(name):
    # load nodes details
    with open(f"../datasets/formatted_for_embeddings/karate/{name}.nodes") as f:
        nodes = f.read().splitlines()

    # load edges (or links)
    with open(f"../datasets/formatted_for_embeddings/karate/{name}.edges") as f:
        links = f.read().splitlines()

    # capture nodes in 2 separate lists
    node_list_1 = []
    node_list_2 = []

    for i in tqdm(links):
        node_list_1.append(i.split(',')[0])
        node_list_2.append(i.split(',')[1])

    df = pd.DataFrame({'node_1': node_list_1, 'node_2': node_list_2})

    # print(df.head())

    return df, node_list_1, node_list_2


def plot_initial_graph(G):
    # plot graph
    plt.figure(figsize=(10, 10))

    pos = nx.random_layout(G, seed=23)
    nx.draw(G, with_labels=False, pos=pos, node_size=40, alpha=0.6, width=0.7)

    plt.show()


def find_unconnected_pairs_from_adj_matrix(G, node_list_1, node_list_2):
    # combine all nodes in a list
    node_list = node_list_1 + node_list_2

    # remove duplicate items from the list
    node_list = list(dict.fromkeys(node_list))

    # build adjacency matrix
    adj_G = nx.to_numpy_matrix(G, nodelist=node_list)

    # print(adj_G)

    all_unconnected_pairs = []

    # traverse adjacency matrix
    offset = 0
    for i in tqdm(range(adj_G.shape[0])):
        for j in range(offset, adj_G.shape[1]):
            if i != j and adj_G[i, j] == 0:
                all_unconnected_pairs.append([node_list[i], node_list[j]])

        offset = offset + 1

    return all_unconnected_pairs


def create_data_from_unconnected(unconnected_pairs):
    node_1_unlinked = [i[0] for i in unconnected_pairs]
    node_2_unlinked = [i[1] for i in unconnected_pairs]

    data = pd.DataFrame({'node_1': node_1_unlinked,
                         'node_2': node_2_unlinked})

    # add target variable 'link'
    data['link'] = 0

    return data


def find_non_existing_links_and_drop(data, df, G):
    temp_df = df.copy()

    initial_node_count = len(G.nodes)

    # empty list to store removable links
    omissible_links_index = []

    for i in tqdm(df.index.values):

        # remove a node pair and build a new graph
        G_temp = nx.from_pandas_edgelist(temp_df.drop(index=i), "node_1", "node_2", create_using=nx.Graph())

        # check there is no spliting of graph and number of nodes is same
        if (nx.number_connected_components(G_temp) == 1) and (len(G_temp.nodes) == initial_node_count):
            omissible_links_index.append(i)
            temp_df = temp_df.drop(index=i)

    # create dataframe of removable edges

    ghost_links = df.loc[omissible_links_index]

    # add the target variable 'link'
    ghost_links['link'] = 1

    data = data.append(ghost_links[['node_1', 'node_2', 'link']], ignore_index=True)

    # drop removable edges
    df_partial = df.drop(index=ghost_links.index.values)

    return data, df_partial


def node_2_vec_features(G_data):
    # Generate walks
    node2vec = Node2Vec(G_data, dimensions=100, walk_length=16, num_walks=50)

    # train node2vec model
    n2w_model = node2vec.fit(window=7, min_count=1)

    return n2w_model


def train_and_get_predictions(x, data):
    xtrain, xtest, ytrain, ytest = train_test_split(np.array(x), data['link'],
                                                    test_size=0.3,
                                                    random_state=35)

    lr = LogisticRegression(class_weight="balanced")

    lr.fit(xtrain, ytrain)

    # print(len(xtrain))
    # print(len(ytrain))
    #
    # print(len(xtest))
    # print(len(ytest))
    #
    # print(len(data))

    predictions = lr.predict_proba(xtest)

    return predictions, ytest


def graph_embeddings(name, verbose):
    df, node_list_1, node_list_2 = load_embeddings(name)

    # create graph
    G = nx.from_pandas_edgelist(df, "node_1", "node_2", create_using=nx.Graph())

    if verbose:
        plot_initial_graph(G)

    unconnected_pairs = find_unconnected_pairs_from_adj_matrix(G, node_list_1, node_list_2)

    data = create_data_from_unconnected(unconnected_pairs)

    data, df_partial = find_non_existing_links_and_drop(data, df, G)

    # build graph
    G_data = nx.from_pandas_edgelist(df_partial, "node_1", "node_2", create_using=nx.Graph())

    n2w_model = node_2_vec_features(G_data)

    x = [(n2w_model[str(i)] + n2w_model[str(j)]) for i, j in zip(data['node_1'], data['node_2'])]

    predictions, ytest = train_and_get_predictions(x, data)

    # print(predictions)
    # print(len(predictions))

    labels = list(ytest)
    indexes = list(ytest.index)

    for i in range(len(ytest)):
        print(f'{indexes[i]}: {predictions[i]} -> {labels[i]}')
