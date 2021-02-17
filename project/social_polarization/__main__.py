from __helpers_pickles__ import open_pickles_for_adjusting_visualization_manually, open_pickles_for_final
from __compute_polarization__ import get_polarization_with_inverse
from __helpers_general__ import format_edge_list_from_tuples
from __drivers__algorithms__ import *


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
    #      6)beefban                          #
    # --------------------------------------- #

    start = time.time()
    name = 'polblogs'
    graph = load_graph(f'../datasets/{name}.gml')
    pol, converged_opinions = get_polarization(graph)
    end = time.time()
    print(end - start)

    # --------------------------------------- #
    #     convert datasets to gml             #
    # --------------------------------------- #

    # convert_datasets_driver()

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
    #    Last argument:                       #
    #    Expected mode:                       #
    #    1) Embeddings                        #
    #    2) Ignore , to not consider          #
    # --------------------------------------- #

    algorithms_2 = ['FTGreedy', 'FTGreedyBatch', 'Expressed Distance', 'Expressed Multiplication', 'Random']
    #

    algorithms = ['Greedy', 'GBatch', 'FTGreedy', 'FTGreedyBatch', 'BExpressed Distance',
                  'BExpressed Multiplication', 'Expressed Distance',
                  'Expressed Multiplication', 'Random']

    algorithms_expressed = ['Expressed Distance', 'Expressed Multiplication', 'BExpressed Distance',
                            'BExpressed Multiplication', 'Random']
    #
    # algorithms1 = ['FTGreedy', 'FTGreedyBatch', 'Expressed Distance',
    #                'Expressed Multiplication', 'Random']

    # datasets = ['polblogs', 'ClintonTrump', 'GermanWings', 'sxsw']

    k = [5, 10, 15, 20]

    # info = algorithms_driver(k=k,
    #                          datasets=['beefban'],
    #                          algorithms=algorithms_2,
    #                          expected_mode='Ignore',
    #                          experiment_comment='find ftgreedy bug')

    info = algorithms_driver(k=k,
                             datasets=['karate'],
                             algorithms=algorithms,
                             expected_mode='Ignore',
                             experiment_comment='small test')
    #
    # info = algorithms_driver(k=k,
    #                          datasets=['books'],
    #                          algorithms=algorithms,
    #                          expected_mode='Embeddings',
    #                          experiment_comment='books experiment embeddings after equal edges')
    #

    # info = algorithms_driver(k=[200, 400, 600, 800],
    #                          datasets=['beefban'],
    #                          algorithms=algorithms_2,
    #                          expected_mode='Ignore',
    #                          experiment_comment='beefban experiment for ftgreedy')
    #
    # info = algorithms_driver(k=[400, 800, 1200, 1600],
    #                          datasets=['polblogs'],
    #                          algorithms=algorithms_2,
    #                          expected_mode='Ignore',
    #                          experiment_comment='polblogs experiment efor ftgreedy')
    #
    # info = algorithms_driver(k=[500, 1000, 1500, 2000],
    #                          datasets=['GermanWings'],
    #                          algorithms=algorithms_2,
    #                          expected_mode='Ignore',
    #                          experiment_comment='GermanWings experiment for ftgreedy')
    #
    # info = algorithms_driver(k=[700, 1400, 2100, 2800],
    #                          datasets=['ClintonTrump'],
    #                          algorithms=algorithms_2,
    #                          expected_mode='Ignore',
    #                          experiment_comment='ClintonTrump experiment for ftgreedy')

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

    # --------------------------------------- #
    #   Prepare final plots                   #
    # --------------------------------------- #

    ##################
    # ! important :  #  don't change position of algorithm labels so they correspond correctly to experiments!
    ##################

    # algorithms = ['Greedy', 'GBatch', 'FTGreedy', 'FTGreedyBatch', 'Expressed Distance',
    #               'Expressed Multiplication', 'Random']
    #
    # open_pickles_for_final([5, 10, 15, 20], ['karate', 'books', 'beefban', 'polblogs', 'ClintonTrump', 'GermanWings'],
    #                        algorithms)


if __name__ == "__main__":
    main()
