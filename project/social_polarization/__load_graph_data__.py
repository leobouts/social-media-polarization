import pandas as pd
from perm import *


def load_graph(gml_file):
    name = gml_file.split("/")[2].split(".")[0]

    graph = nx.read_gml(gml_file, label='id')

    graph = nx.Graph(graph, name=name)

    return graph


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
    multiplication = []

    for i in links:
        node_1_value = nodeDict[i.split(',')[0]]['value']
        node_2_value = nodeDict[i.split(',')[1]]['value']

        node_list_1.append(i.split(',')[0])
        node_list_2.append(i.split(',')[1])
        distance_abs = abs(int(node_1_value) - int(node_2_value))
        mult = int(node_1_value) * int(node_2_value)

        distance.append(distance_abs)
        multiplication.append(mult)

    df = pd.DataFrame(
        {'node_1': node_list_1, 'node_2': node_list_2, 'distance': distance, 'multiplication': multiplication})

    return df, nodeDict
