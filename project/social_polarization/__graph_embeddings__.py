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

from __helpers__ import add_edges_and_count_polarization, load_embeddings, get_positive_and_negative_values

simplefilter("ignore", category=ConvergenceWarning)


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

    # Generate walks
    node2vec = Node2Vec(G_data, dimensions=100, walk_length=16, num_walks=50, quiet=True)

    # get the embeddings model using gensim's Word2V
    # from fitting node2vec.fit
    n2w_model = node2vec.fit(window=7, min_count=1)

    x = [(n2w_model[str(i)] + n2w_model[str(j)]) for i, j in zip(result['node_1'], result['node_2'])]

    xtrain, xtest, ytrain, ytest = train_test_split(np.array(x), result['link'],
                                                    test_size=0.2,
                                                    random_state=35)

    lr = LogisticRegression(class_weight="balanced", n_jobs=-1, solver='sag')

    lr.fit(xtrain, ytrain)

    edges_list = []
    probabilities_list = []

    # drop all edges that exist, we need edges that were not present.
    result.drop(result.loc[result['link'] == 1].index, inplace=True)

    # predict the probabilities for each label, first column for 0 label, second for 1
    predictions = lr.predict_proba(x)

    # find where the pairs are located and their result
    for i in range(len(data)):
        try:
            pair = (int(result.iloc[i, 0]), int(result.iloc[i, 1]))

            edges_list.append(pair)

            probabilities_list.append(float(predictions[i][1]) * 100)

            if verbose:
                print(
                    f'Probability of nodes {result.iloc[i, 0]} and {result.iloc[i, 1]} to form a link is : '
                    f'{float(predictions[i][1]) * 100 : .2f}%')
        except:
            continue

    keydict = dict(zip(edges_list, probabilities_list))
    edges_list.sort(key=keydict.get)

    return edges_list
