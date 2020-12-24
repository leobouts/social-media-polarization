from __compute_polarization__ import get_polarization_with_inverse
from __drivers__ import *
from __helpers__ import format_edge_list_from_tuples, \
    open_pickles_for_adjusting_visualization_manually, open_info_pickle


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

    name = 'ClintonTrump'
    graph = load_graph(f'../datasets/{name}.gml')

    # pol, converged_opinions = get_polarization(graph)
    # print(pol)
    # print(get_polarization_with_inverse(graph))

    # --------------------------------------- #
    #     convert datasets to gml             #
    # --------------------------------------- #

    # convert_datasets_driver()

    # --------------------------------------- #
    #   creates files needed for embeddings   #
    #   from the networkx graphs.             #
    #   An edge list and a node list.         #
    # --------------------------------------- #

    # convert_networkx_to_txt_for_embeddings_driver()

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
    #     3) FTGreedy                         #
    #     4) FTGreedyBatch                    #
    #     5) Expressed Distance               #
    #     6) Expressed Multiplication         #
    #     7) Random                           #
    # --------------------------------------- #
    #    k: list with top-k edges to add      #
    # --------------------------------------- #
    #    Last argument :                      #
    #    Expected mode, available:            #
    #    1) common_neighbors                  #
    #    2) Jaccard_coefficient               #
    #    3) Adamic_addar_index                #
    #    4) Embeddings                        #
    #    5) Ignore , to not consider          #
    # --------------------------------------- #

    k = [5, 10, 15, 20]

    algorithms = ['Greedy', 'GBatch', 'FTGreedyBatch', 'Random', 'Expressed Distance',
                  'Expressed Multiplication']

    #algorithms1 = ['Expressed Distance', 'Expressed Multiplication', 'Random']

    #datasets = ['karate', 'polblogs', 'books', 'ClintonTrump', 'GermanWings', 'sxsw', 'beefban']

    info = algorithms_driver(k, ['karate'], algorithms, 'Ignore')

    # ------------------------------------------------------- #
    # open information from previous experiments              #
    # ------------------------------------------------------- #

    #info = open_info_pickle('karate')

    ######################################################################
    # to Access information returned by edge additions                   #
    # you have to specify this : info['{algorithm}_{ds}_{k_edges}'][x]   #
    # where x can be 'result_dictionary', 'time', 'polarization'         #
    ######################################################################

    #edge_list = (info['Greedy_karate_10']['result_dictionary'])

    #convert the tuple list into the format that visualize_edge takes

    #edge_list = format_edge_list_from_tuples(edge_list)

    # ------------------------------------------------------- #
    # visualize graph edges, mode = 1 addition, = 0 removal   #
    # ------------------------------------------------------- #

    #visualize_edge(graph, edge_list, "top-10 edge addition in Karate from Greedy",
    #               "Greedy_karate_10", "karate", 1)

    # ---------------------------------------- #
    #     re-draw graph from pickles data for  #
    #     manually adjusting it (if needed)    #
    # ---------------------------------------- #
    #  First arg: the k list                   #
    #  Second arg: the dataset name            #
    # ---------------------------------------- #

    #open_pickles_for_adjusting_visualization_manually([5, 10, 20, 30], 'karate')

    # --------------------------------------- #
    #     Fully connected for lemma 5.1       #
    # --------------------------------------- #

    # fully_connected_graph = make_graph_fully_connected(graph)
    #pol, converged_opinions = get_polarization(fully_connected_graph)

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
