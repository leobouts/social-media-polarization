from __compute_polarization__ import get_polarization_with_inverse
from __drivers__algorithms__ import *
from __helpers_general__ import format_edge_list_from_tuples
from __helpers_pickles__ import open_pickles_for_adjusting_visualization_manually, open_pickles_for_final


def main():
    # --------------------------------------- #
    #      Test Graph Init                    #
    # --------------------------------------- #
    # --------------------------------------- #
    #      Available Datasets:                #
    # --------------------------------------- #
    #      0)test                             #
    #        (example from thesis increase)   #
    #      1)karate                           #
    #      2)polblogs                         #
    #      3)books                            #
    #      4)ClintonTrump                     #
    #      5)GermanWings                      #
    #      6)beefban                          #
    # --------------------------------------- #

    name = 'karate_zero'
    graph = load_graph(f'../datasets/{name}.gml')

    pol, converged_opinions = get_polarization_with_inverse(graph)

    # print("polarization: ",pol)
    # print("z vector: ", converged_opinions)
    # print("sum: ", sum(converged_opinions))
    #
    # print("--------")
    # print("karate zero:")
    #
    # name = 'karate_zero'
    # graph = load_graph(f'../datasets/{name}.gml')
    #
    # pol, converged_opinions = get_polarization_with_inverse(graph)
    # print("polarization: ", pol)
    # print("z vector: ", converged_opinions)
    # print("sum: ", sum(converged_opinions))
    # print(pol)
    # print(get_polarization_with_inverse(graph)[1])

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
    #     8) Random different                 #
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

    # ! important don't change position of algorithm lables so they correspond correctly!
    # algorithms = ['Greedy', 'GBatch', 'FTGreedy', 'FTGreedyBatch', 'Expressed Distance',
    #               'Expressed Multiplication', 'Random']
    # open_pickles_for_final([5, 10, 15, 20], ['karate', 'books', 'beefban', 'polblogs', 'ClintonTrump', 'GermanWings'],
    #                        algorithms)

    # k = [5]

    # algorithms = ['Random', 'Random different', 'Expressed Distance']

    algorithms = ['GBatch', 'FTGreedy', 'FTGreedyBatch', 'Expressed Distance',
                  'Expressed Multiplication', 'Random']

    algorithms1 = ['FTGreedy', 'FTGreedyBatch', 'Expressed Distance',
                   'Expressed Multiplication', 'Random']
    #
    # # datasets = ['polblogs', 'ClintonTrump', 'GermanWings', 'sxsw']
    #

    info = algorithms_driver(k=[5, 10, 15, 20],
                             datasets=['books'],
                             algorithms=algorithms,
                             expected_mode='Embeddings',
                             experiment_comment='karate experiment embeddings')

    # info = algorithms_driver(k=[5, 10, 15, 20],
    #                          datasets=['karate'],
    #                          algorithms=algorithms,
    #                          expected_mode='Ignore',
    #                          experiment_comment='karate experiment final ver1')

    # info = algorithms_driver(k=[5, 10, 15, 20],
    #                          datasets=['beefban', 'polblogs', 'ClintonTrump', 'GermanWings'],
    #                          algorithms=algorithms1,
    #                          expected_mode='Ignore',
    #                          experiment_comment='experiments for final plots 2')

    # ------------------------------------------------------- #
    # open information from previous experiments              #
    # ------------------------------------------------------- #

    # info = open_info_pickle('karate')

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

    # visualize_edge(graph, edge_list, "top-10 edge addition in Karate from Greedy",
    #               "Greedy_karate_10", "karate", 1)

    # ---------------------------------------- #
    #     re-draw graph from pickles data for  #
    #     manually adjusting it (if needed)    #
    # ---------------------------------------- #
    #  First arg: the k list                   #
    #  Second arg: the dataset name            #
    #  Third argument: experiment time (file)  #
    # ---------------------------------------- #

    # open_pickles_for_adjusting_visualization_manually([5, 10, 15, 20], 'ClintonTrump', "enter experiment time here")

    # --------------------------------------- #
    #     Fully connected for lemma 5.1       #
    # --------------------------------------- #

    # fully_connected_graph = make_graph_fully_connected(graph)
    # pol, converged_opinions = get_polarization(fully_connected_graph)

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
