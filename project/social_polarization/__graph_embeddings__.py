from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from __load_graph_data__ import load_graph
from warnings import simplefilter
from node2vec import Node2Vec
import networkx as nx
import pandas as pd
import numpy as np


simplefilter("ignore", category=ConvergenceWarning)


def graph_embeddings(name, verbose):

    graph = load_graph(f'../datasets/{name}.gml')

    node_list_1 = []
    node_list_2 = []

    for edge in graph.edges():
        node_list_1.append(str(edge[0]))
        node_list_2.append(str(edge[1]))

    df = pd.DataFrame({'node_1': node_list_1, 'node_2': node_list_2})

    node_1_unlinked = []
    node_2_unlinked = []

    for e in nx.non_edges(graph):
        node_1_unlinked.append(str(e[0]))
        node_2_unlinked.append(str(e[1]))

    data = pd.DataFrame({'node_1': node_1_unlinked, 'node_2': node_2_unlinked})


    # add target variable 'link'
    data['link'] = 0

    # get equal number of edges that don't exist so
    # we don't create a class imbalance

    num_of_existing_edges = len(list(graph.edges()))
    equal_nonexisting_edges_df = data.sample(n=num_of_existing_edges)

    # create new dataframe from edges that exist with a label of 1
    new_data = df
    new_data['link'] = 1

    # concatenate these two into a single dataframe
    result = pd.concat([new_data, equal_nonexisting_edges_df])
    result.reset_index(inplace=True, drop=True)

    # Generate walks with default parameters
    node2vec = Node2Vec(graph, quiet=False)

    # get the embeddings model using gensim's Word2V
    # from fitting node2vec.fit
    n2w_model = node2vec.fit(min_count=1)

    # zip creates a list of all the edges from the result df
    # n2w_model with an input of a string(the name of the node, e.g. node '1'), will give us the
    # features returned from the embeddings.
    # for this case we add the features of the the nodes together so we can pass a single
    # feature list in the logistic regression

    x = [(n2w_model[str(i)] + n2w_model[str(j)]) for i, j in zip(result['node_1'], result['node_2'])]

    # For the training of the classifier we use as train test the 80% of the network’s edges for
    # positive examples and equal amount of edges that don’t exist for negative example. We use the rest 20% of
    # positive edges and equal amount of negative edges as test set.

    xtrain, xtest, ytrain, ytest = train_test_split(np.array(x), result['link'],
                                                    test_size=0.2,
                                                    random_state=35)

    lr = LogisticRegression()

    lr.fit(xtrain, ytrain)

    edges_list = []
    probabilities_list = []

    x_2 = [(n2w_model[str(i)] + n2w_model[str(j)]) for i, j in zip(data['node_1'], data['node_2'])]

    # predict the probabilities for each label, first column for 0 label, second for 1
    predictions = lr.predict_proba(x_2)

    # find where the pairs are located and their result
    for i in range(len(data.index)):

        pair = (int(data.iloc[i, 0]), int(data.iloc[i, 1]))
        edges_list.append(pair)

        probabilities_list.append(float(predictions[i][1]))

        if verbose:
            print(
                f'Probability of nodes {data.iloc[i, 0]} and {data.iloc[i, 1]} to form a link is : '
                f'{float(predictions[i][1]) * 100 : .2f}%')

    keydict = dict(zip(edges_list, probabilities_list))
    edges_list.sort(key=keydict.get)

    return edges_list, probabilities_list
