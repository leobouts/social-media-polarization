from __helpers__ import get_positive_and_negative_values
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from __load_graph_data__ import load_embeddings
from warnings import simplefilter
from node2vec import Node2Vec
import networkx as nx
import pandas as pd
import numpy as np


simplefilter("ignore", category=ConvergenceWarning)


def create_data_from_unconnected(G, nodeDict):
    node_1_unlinked = []
    node_2_unlinked = []

    pos_nodes, neg_nodes = get_positive_and_negative_values(nodeDict)

    for p in pos_nodes:
        for n in neg_nodes:
            node_1_unlinked.append(p[0])
            node_2_unlinked.append(n[0])

    data = pd.DataFrame({'node_1': node_1_unlinked, 'node_2': node_2_unlinked})

    # add target variable 'link'
    data['link'] = 0

    return data


def graph_embeddings(name, verbose):
    df, nodeDict = load_embeddings(name)

    # create graph
    G_data = nx.from_pandas_edgelist(df, "node_1", "node_2", create_using=nx.Graph())

    # get all edges that don't exist with a label of 0
    data = create_data_from_unconnected(G_data, nodeDict)

    # create new dataframe form edges that exist with a label of 1
    new_data = df.drop(['distance', 'multiplication'], 1)
    new_data['link'] = 1

    # concatenate these two into a single dataframe
    result = pd.concat([data, new_data])
    result.reset_index(inplace=True, drop=True)

    # Generate walks
    node2vec = Node2Vec(G_data, dimensions=100, walk_length=16, num_walks=50, quiet=False)

    # get the embeddings model using gensim's Word2V
    # from fitting node2vec.fit
    n2w_model = node2vec.fit(window=7, min_count=1)

    # zip creates a list of all the edges from the result df
    # n2w_model with an input of a string(the name of the node, e.g. node '1'), will give us the
    # features returned from the embeddings.
    # for this case we add the features of the the nodes together so we can pass a single
    # feature list in the logistic regression
    x = [(n2w_model[str(i[0])] + n2w_model[str(j[0])]) for i, j in zip(result['node_1'], result['node_2'])]

    # For the training of the classifier we use as train test the 80% of the network’s edges for
    # positive examples and equal amount of edges that don’t exist for negative example. We use the rest 20% of
    # positive edges and equal amount of negative edges as test set.

    xtrain, xtest, ytrain, ytest = train_test_split(np.array(x), result['link'],
                                                    test_size=0.2,
                                                    random_state=35)

    lr = LogisticRegression(class_weight="balanced", n_jobs=-1, solver='sag')

    lr.fit(xtrain, ytrain)

    edges_list = []
    probabilities_list = []

    # drop all edges that exist, we need edges that were not present.
    result = result.drop(result.loc[result['link'] == 1].index, inplace=False)
    x_2 = [(n2w_model[str(i[0])] + n2w_model[str(j[0])]) for i, j in zip(result['node_1'], result['node_2'])]

    # predict the probabilities for each label, first column for 0 label, second for 1
    predictions = lr.predict_proba(x_2)

    # find where the pairs are located and their result
    for i in range(len(result.index)):

        pair = (int(result.iloc[i, 0]), int(result.iloc[i, 1]))
        edges_list.append(pair)

        probabilities_list.append(float(predictions[i][1]))

        if verbose:
            print(
                f'Probability of nodes {result.iloc[i, 0]} and {result.iloc[i, 1]} to form a link is : '
                f'{float(predictions[i][1]) * 100 : .2f}%')

    keydict = dict(zip(edges_list, probabilities_list))
    edges_list.sort(key=keydict.get)

    return edges_list, probabilities_list
