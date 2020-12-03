import pandas as pd
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
from node2vec import Node2Vec

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import f1_score, auc, roc_curve, roc_auc_score
from warnings import simplefilter
from sklearn.exceptions import ConvergenceWarning
from tqdm import tqdm

from __helpers__ import add_edges_and_count_polarization

simplefilter("ignore", category=ConvergenceWarning)


def load_embeddings(name):
    # load nodes details
    with open(f"../datasets/formatted_for_embeddings/{name}/{name}.nodes") as f:
        nodes = f.read().splitlines()

    # load edges (or links)
    with open(f"../datasets/formatted_for_embeddings/{name}/{name}.edges") as f:
        links = f.read().splitlines()

    nodeDict = {}
    count = 0
    for i in nodes:

        if count == 0:
            count = 1
            continue

        splitted_vals = i.split(",")
        nodeDict[splitted_vals[0]] = {'value': splitted_vals[1]}

    # capture nodes in 2 separate lists
    node_list_1 = []
    node_list_2 = []
    distance = []

    for i in links:
        node_1_value = nodeDict[i.split(',')[0]]['value']
        node_2_value = nodeDict[i.split(',')[1]]['value']

        node_list_1.append(i.split(',')[0])
        node_list_2.append(i.split(',')[1])

        distance.append(abs(int(node_1_value) - int(node_2_value)))

    df = pd.DataFrame({'node_1': node_list_1, 'node_2': node_list_2, 'distance': distance})

    # print(df.head())

    return df, node_list_1, node_list_2, nodeDict


def plot_initial_graph(G):
    # plot graph
    plt.figure(figsize=(10, 10))

    pos = nx.random_layout(G, seed=23)
    nx.draw(G, with_labels=False, pos=pos, node_size=40, alpha=0.6, width=0.7)

    plt.show()


def create_data_from_unconnected(G, nodeDict):
    unconnected_pairs = nx.non_edges(G)
    node_1_unlinked = []
    node_2_unlinked = []

    for i in unconnected_pairs:
        if int(nodeDict[i[0]]['value']) * int(nodeDict[i[1]]['value']) < 0:
            node_1_unlinked.append(i[0])
            node_2_unlinked.append(i[1])

    data = pd.DataFrame({'node_1': node_1_unlinked, 'node_2': node_2_unlinked})

    # add target variable 'link'
    data['link'] = 0

    return data


def find_non_existing_links_and_drop(data, df, G, nodeDict):
    temp_df = df.copy()
    initial_node_count = len(G.nodes)

    # empty list to store removable links
    omissible_links_index = []

    # sort the values by distance so we can drop them by the biggest distance
    df = df.sort_values(by=['distance'])

    # print(df.head())

    count = 0
    for i in tqdm(df.index.values):

        # remove a node pair and build a new graph
        G_temp = nx.from_pandas_edgelist(temp_df.drop(index=i), "node_1", "node_2", create_using=nx.Graph())

        # check there is no spliting of graph and number of nodes is same
        if (nx.number_connected_components(G_temp) == 1) and (len(G_temp.nodes) == initial_node_count):
            node_1 = df["node_1"].iloc[i]
            node_2 = df["node_2"].iloc[i]

            if int(nodeDict[node_1]['value']) * int(nodeDict[node_2]['value']) < 0:
                omissible_links_index.append(i)
                temp_df = temp_df.drop(index=i)
                count += 1

        # break when we have dropped the first % of the nodes that could be dropped
        #if count >= len(df.index.values) * 0.2:
        #    break

    # create dataframe of removable edges
    ghost_links = df.loc[omissible_links_index]

    # add the target variable 'link'
    ghost_links['link'] = 1

    data = data.append(ghost_links[['node_1', 'node_2', 'link']], ignore_index=True)

    # drop removable edges
    df_partial = df.drop(index=ghost_links.index.values)

    return data, df_partial, ghost_links


def node_2_vec_features(G_data):
    # Generate walks
    node2vec = Node2Vec(G_data, dimensions=100, walk_length=16, num_walks=50, quiet=False)

    # train node2vec model
    n2w_model = node2vec.fit(window=7, min_count=1)

    return n2w_model


def graph_embeddings(name, verbose):
    df, node_list_1, node_list_2, nodeDict = load_embeddings(name)

    # create graph
    G = nx.from_pandas_edgelist(df, "node_1", "node_2", create_using=nx.Graph())

    if verbose:
        plot_initial_graph(G)

    data = create_data_from_unconnected(G, nodeDict)

    data, df_partial, ghost_links = find_non_existing_links_and_drop(data, df, G, nodeDict)

    # build graph
    G_data = nx.from_pandas_edgelist(df_partial, "node_1", "node_2", create_using=nx.Graph())

    n2w_model = node_2_vec_features(G_data)

    x = [(n2w_model[str(i)] + n2w_model[str(j)]) for i, j in zip(data['node_1'], data['node_2'])]

    xtrain, xtest, ytrain, ytest = train_test_split(np.array(x), data['link'],
                                                    test_size=0.2,
                                                    random_state=35)

    lr = LogisticRegression(class_weight="balanced", n_jobs=-1, solver='sag')

    lr.fit(xtrain, ytrain)

    edges_list = []
    probabilities_list = []

    # drop all edges that were in the graph, we need edges that were not present.
    data.drop(data.loc[data['link'] == 1].index, inplace=True)

    predictions = lr.predict_proba(x)

    #print(predictions)

    for i in tqdm(range(len(data))):
        try:

            # # data correspond to x
            # # we need to find where the x[i] exists in the train set
            # index_in_x_train = np.where(xtrain == x[i])[0][1]
            #
            # # reshaping just adds the list of features inside an empty list so : [list of features]
            # # needed to be passed in the predict_proba.
            # # [:, 1] advanced indexing for numpy, : gets all rows. ",1" gets only the items of the first column
            # # e.g. [:, [1,2]] would bring all rows but only with columns 1 and 2.
            #
            # # The first column is the probability  of predict_proba says that the entry has the 0 label and the second
            # # column is the probability that the entry has the 1 label.
            #
            # predict_proba = lr.predict_proba(xtrain[index_in_x_train].reshape(1, -1))[:, 1]
            pair = (int(data.iloc[i, 0]), int(data.iloc[i, 1]))

            edges_list.append(pair)
            # probabilities_list.append(float(predict_proba) * 100)

            probabilities_list.append(float(predictions[i][1])*100)

            if verbose:
                print(
                    f'Probability of nodes {data.iloc[i, 0]} and {data.iloc[i, 1]} to form a link is : {float(predictions[i][1]) * 100 : .2f}%')
        except:
            continue

    keydict = dict(zip(edges_list, probabilities_list))
    edges_list.sort(key=keydict.get)

    return edges_list
