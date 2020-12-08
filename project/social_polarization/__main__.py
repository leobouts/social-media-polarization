from __drivers__ import *
from __helpers__ import format_edge_list_from_tuples, get_nodes_and_values_from_nx_to_txt


def main():

    # --------------------------------------- #
    #      Test Graph Init                    #
    # --------------------------------------- #
    # --------------------------------------- #
    #      Available Datasets:                #
    # --------------------------------------- #
    #      1)karate                           #
    #      2)polblogs                         #
    #      3)books                            #
    #      4)ClintonTrump                     #
    #      5)GermanWings                      #
    #      6)sxsw                             #
    #      7)beefban                          #
    # --------------------------------------- #

    #name = 'karate'
    #graph = load_graph(f'../datasets/{name}.gml')
    #print(get_polarization(graph))

    # --------------------------------------- #
    #     convert datasets to gml             #
    # --------------------------------------- #

    # convert_datasets_driver()

    # --------------------------------------- #
    #   creates files needed for embeddings   #
    #   from the networkx graphs.             #
    #   An edge list and a node list.         #
    # --------------------------------------- #

    # convert_networkx_to_txt_for_embeddings_driver(graph, name)

    # --------------------------------------- #
    # function that supports Lemma 3.1        #
    # --------------------------------------- #

    # find_increase_in_graphs_with_addition()

    # --------------------------------------- #
    #     Algorithms experiment               #
    # --------------------------------------- #
    # --------------------------------------- #
    #     Available Algorithms:               #
    # --------------------------------------- #
    #     1) Greedy                           #
    #     2) GBatch                           #
    #     3) FKGreedy                         #
    #     4) Expressed Distance               #
    #     5) Expressed Multiplication         #
    # --------------------------------------- #
    #    k: list with top-k edges to add      #
    # --------------------------------------- #

    k = [5, 10, 15, 20]
    algorithms = ['GBatch', 'FKGreedy', 'Expressed Distance', 'Expressed Multiplication']

    # datasets = ['karate', 'polblogs', 'books', 'ClintonTrump', 'GermanWings', 'sxsw', 'beefban']

    info = algorithms_driver(k, ['karate'], ['GBatch'])

    ######################################################################
    # to Access information returned by edge additions                   #
    # you have to specify this : info['{algorithm}_{ds}_{k_edges}'][x]   #
    # where x can be 'result_dictionary', 'time', 'polarization'         #
    ######################################################################

    # edge_list = (info['Greedy_karate_10']['result_dictionary'])

    # convert the tuple list into the format that visualize_edge takes

    # edge_list = format_edge_list_from_tuples(edge_list)

    # ------------------------------------------------------- #
    # visualize graph edges, mode = 1 addition, = 0 removal   #
    # ------------------------------------------------------- #

    # visualize_edge(graph, edge_list, "top-10 edge addition in books from Greedy",
    #               "top-10_karate_greedy", 1)

    # --------------------------------------- #
    #     Fully connected for lemma 5.1       #
    # --------------------------------------- #

    # fully_connected_graph = make_graph_fully_connected(graph)
    # print(get_polarization(fully_connected_graph))

    # --------------------------------------- #
    #              edge removals              #
    # --------------------------------------- #

    # edge_removals_driver(graph, name)

    # --------------------------------------- #
    #              dataset statistics         #
    #              verbose = 1 prints them    #
    # --------------------------------------- #

    # ds_stats = dataset_statistics_driver(datasets, 1)


if __name__ == "__main__":
    main()
