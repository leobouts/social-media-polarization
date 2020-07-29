from numpy import linalg as LA
import networkx as nx


def check_properties(graph, decrease_dictionary):

    nodes_to_check = []

    sorted_dict = sorted(decrease_dictionary)

    smallest_10_decrease = sorted_dict[:10]
    biggest_10_decrease = sorted_dict[-10:]

    top_decrease_nodes = []
    small_decrease_nodes = []

    for value in biggest_10_decrease:

        decrease = decrease_dictionary[value]
        nodes = decrease['addition'].split('->')
        top_decrease_nodes.append(nodes[0])
        top_decrease_nodes.append(nodes[1])

    for value in smallest_10_decrease:

        decrease = decrease_dictionary[value]
        nodes = decrease['addition'].split('->')
        small_decrease_nodes.append(nodes[0])
        small_decrease_nodes.append(nodes[1])

    # remove duplicate nodes
    top_decrease_nodes = list(dict.fromkeys(top_decrease_nodes))
    small_decrease_nodes = list(dict.fromkeys(small_decrease_nodes))

    # map the to int so they can be sorted and accessed
    top_decrease_nodes = list(map(int, top_decrease_nodes))
    small_decrease_nodes = list(map(int, small_decrease_nodes))

    top_decrease_nodes = sorted(top_decrease_nodes)
    small_decrease_nodes = sorted(small_decrease_nodes)


    # holds centrality values of every node
    closeness_c = nx.closeness_centrality(graph)
    betweenness_c = nx.betweenness_centrality(graph)
    eigen_centrality = nx.eigenvector_centrality(graph)

    top_node_closeness_c = [closeness_c[node] for node in top_decrease_nodes]
    top_node_betweeness = [betweenness_c[node] for node in top_decrease_nodes]
    top_node_eigen = [eigen_centrality[node] for node in top_decrease_nodes]

    small_node_closeness_c = [closeness_c[int(node)] for node in small_decrease_nodes]
    small_node_betweeness = [betweenness_c[int(node)] for node in small_decrease_nodes]
    small_node_eigen = [eigen_centrality[node] for node in small_decrease_nodes]

    print("-----largest decrease------")
    print(top_decrease_nodes)
    print(top_node_closeness_c)
    print(LA.norm(top_node_closeness_c))
    print(top_node_betweeness)
    print(LA.norm(top_node_betweeness))
    print(top_node_eigen)
    print(LA.norm(top_node_eigen))


    print("-----smallest decrease------")

    print(small_decrease_nodes)
    print(small_node_closeness_c)
    print(LA.norm(small_node_closeness_c))
    print(small_node_betweeness)
    print(LA.norm(small_node_betweeness))
    print(small_node_eigen)
    print(LA.norm(small_node_eigen))


    # max centralities of the whole graph
    node_with_max_closeness_c = max(closeness_c, key=closeness_c.get)
    node_with_max_betweenness_c = max(betweenness_c, key=betweenness_c.get)

    # Compute node connectivity between all pairs of nodes.
    connectivities = nx.all_pairs_node_connectivity(graph)

    ##########################################################################################