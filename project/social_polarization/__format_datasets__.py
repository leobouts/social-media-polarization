import networkx as nx


def conservative_liberal_conversion(g):
    value_dictionary = nx.get_node_attributes(g, 'value')

    # empty dictionary
    attrs = {}

    for key, value in value_dictionary.items():
        # c = conservative, l=liberal, n=neutral

        if value_dictionary[key] == "c":
            value_dictionary[key] = 1

        elif value_dictionary[key] == "l":
            value_dictionary[key] = -1

        else:
            value_dictionary[key] = 0

        d = {key: {'value': value_dictionary[key]}}
        attrs.update(d)

    nx.set_node_attributes(g, attrs)

    return g


def zero_value_conversion(g):
    # get the values of the new graph in a dictionary
    value_dictionary = nx.get_node_attributes(g, 'value')

    # opinions vary from 0 to 1, find all zero occurences
    zero_indices = [k for (k, v) in value_dictionary.items() if v == 0]

    # empty dictionary
    attrs = {}

    # create the dictionary that will update 0 nodes to -1
    for obj in zero_indices:
        d = {obj: {'value': -1}}
        attrs.update(d)

    # se the new opinion values
    nx.set_node_attributes(g, attrs)

    return g


def adjust_gml_ids_and_values(g, name_to_save):
    '''
    If the  values are in the [0,1] the function can change them to [-1,1] by turning the zeros into negatives.
    If the values are ["c", "l', "n'], conservative, liberal or neutral the function changes them into -1, 0, 1
    accordingly with the conservative_liberal_conversion() method

    If we wan to add a new dataset that has [0,1] or ["c", "l', "n'] values we need to specify that it
    will be changed in the lists bellow.
    '''

    tuples_list = list(g.edges())

    # adjust ids for the edges e.g. edge (2,3) will become edge (1,2)
    if name_to_save == 'karate' or name_to_save == 'polblogs':
        tuples_list = [(edge[0] - 1, edge[1] - 1) for edge in tuples_list]

    nodeDict = dict(g.nodes(data=True))

    zero_value_convert = ['GermanWings', 'beefban', 'sxsw', 'polblogs', 'beefban', 'karate']
    conservative_liberal = ['books', 'ClintonTrump']

    with open(f'../datasets/{name_to_save}.gml', 'w') as the_file:

        the_file.write('graph\n')
        the_file.write('[\n')

        if "ClintonTrump" in name_to_save:
            the_file.write('  directed 0\n')

        for i, node in enumerate(nodeDict):

            the_file.write('  node\n')
            the_file.write('  [\n')
            the_file.write(f'    id {i}\n')

            if name_to_save == 'karate':
                the_file.write(f'    label "{node}"\n')
            else:
                the_file.write(f'    label "{nodeDict[node]["label"]}"\n')

            if name_to_save in conservative_liberal:

                the_file.write(f'    value {nodeDict[node]["value"]}\n')

            elif name_to_save in zero_value_convert:

                if nodeDict[node]["value"] == 0:
                    the_file.write(f'    value -1\n')
                else:
                    the_file.write(f'    value 1\n')

            if name_to_save == 'polblogs':
                the_file.write(f'    source "{nodeDict[node]["source"]}"\n')

            the_file.write('  ]\n')

        for edge in tuples_list:
            the_file.write('  edge\n')
            the_file.write('  [\n')
            the_file.write(f'    source {edge[0]}\n')
            the_file.write(f'    target {edge[1]}\n')
            the_file.write('  ]\n')
        the_file.write(']\n')


def convert_dataset_to_gml(node_values_path, edges_path, name_to_save):
    f = open(node_values_path, "r")
    label_list = []
    value_list = []
    tuples_list = []

    for x in f:
        splitted = x.rstrip().split(",")
        label_list.append(splitted[0])
        value_list.append(splitted[1])

    f = open(edges_path, "r")

    if "ClintonTrump" not in name_to_save:
        for x in f:
            splitted = x.rstrip().split(",")
            edge_1 = splitted[0]
            edge_2 = splitted[1]
            tuples_list.append((edge_1, edge_2))
    else:
        for x in f:
            splitted = x.rstrip().split(" ")
            edge_1 = splitted[0]
            edge_2 = splitted[1]
            tuples_list.append((edge_1, edge_2))

    with open(f'../datasets/{name_to_save}', 'w') as the_file:

        the_file.write('graph\n')
        the_file.write('[\n')

        if "ClintonTrump" in name_to_save:
            the_file.write('  directed 0\n')

        for i, node in enumerate(label_list):

            the_file.write('  node\n')
            the_file.write('  [\n')
            the_file.write(f'    id {i}\n')
            the_file.write(f'    label "{node}"\n')
            if "ClintonTrump" in name_to_save:
                the_file.write(f'    value "{value_list[i]}"\n')
            else:
                the_file.write(f'    value {value_list[i]}\n')
            the_file.write('  ]\n')

        for edge in tuples_list:
            the_file.write('  edge\n')
            the_file.write('  [\n')
            the_file.write(f'    source {label_list.index(edge[0])}\n')
            the_file.write(f'    target {label_list.index(edge[1])}\n')
            the_file.write('  ]\n')
        the_file.write(']\n')


def get_nodes_and_values_from_nx_to_txt(graph, name):
    with open(f'../datasets/formatted_for_embeddings/{name}/{name}.nodes', 'w') as the_file:
        the_file.write('id,value\n')

        for node_data in graph.nodes.data():
            the_file.write(f'{node_data[0]},{node_data[1]["value"]}\n')

    with open(f'../datasets/formatted_for_embeddings/{name}/{name}.edges', 'w') as the_file:

        for edge in graph.edges:
            the_file.write(f'{edge[0]},{edge[1]}\n')