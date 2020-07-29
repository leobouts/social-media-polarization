
######################################
#    possible properties to check    #
######################################

# holds centrality values of every node
closeness_c = nx.closeness_centrality(graph)
betweenness_c = nx.betweenness_centrality(graph)

# max centralities of the whole graph
node_with_max_closeness_c = max(closeness_c, key=closeness_c.get)
node_with_max_betweenness_c = max(betweenness_c, key=betweenness_c.get)

# holds the centralities of negative values
negative_clossenes_c = {k: v for k, v in closeness_c.items() if k not in positive_indices}

# holds the centralities of positive values
positive_clossenes_c = {k: v for k, v in closeness_c.items() if k not in negative_indices}

most_central_node_of_positive = max(positive_clossenes_c, key=positive_clossenes_c.get)
most_central_node_of_negative = max(negative_clossenes_c, key=negative_clossenes_c.get)

# Compute node connectivity between all pairs of nodes.
connectivities = nx.all_pairs_node_connectivity(graph)

##########################################################################################