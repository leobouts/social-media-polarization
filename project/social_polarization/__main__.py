from __drivers__ import *


def main():

    # --------------------------------------- #
    #     convert datasets to gml             #
    # --------------------------------------- #

    # convert_datasets_driver()

    # --------------------------------------- #
    # function that supports Lemma 3.1        #
    # --------------------------------------- #

    # find_increase_in_graphs_with_addition()

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

    name = 'karate'
    graph = load_graph(f'../datasets/{name}.gml')
    print(get_polarization(graph))

    # --------------------------------------- #
    #     Heuristics experiment               #
    # --------------------------------------- #
    # --------------------------------------- #
    #     Available Algorithms:               #
    # --------------------------------------- #
    #     1) Greedy                           #
    #     2) GBatch                           #
    #     3) Skip                             #
    #     4) Distance                         #
    #     5) DME                              #
    #     6) MME                              #
    # --------------------------------------- #
    #    k: list with top-k edges to add      #
    # --------------------------------------- #

    k = [5, 10, 15, 20]

    algorithms = ["Greedy", "GBatch", "Skip", "Distance", "DME", "MME"]
    algorithms1 = ["Distance"]

    datasets = ["karate"]
    info = heuristic_driver(k, datasets, algorithms)

    ######################################################################
    # to Access information returned by edge additions                   #
    # you have to specify this : info['{algorithm}_{ds}_{k_edges}'][x]   #
    # where x can be 'result_dictionary', 'time', 'polarization'         #
    ######################################################################

    edge_list = (info['Greedy_karate_10']['result_dictionary'])

    # convert the tuple list into the format that visualize_edge takes

    edge_list = [f'{e[0]},{e[1]}' for e in edge_list]

    # ------------------------------------------------------- #
    # visualize graph edges, mode = 1 addition, = 0 removal   #
    # ------------------------------------------------------- #

    visualize_edge(graph, edge_list, "top-10 edge addition from Greedy",
                   "top-10_greedy", 1)

    # --------------------------------------- #
    #     Fully connected for lemma 5.1       #
    # --------------------------------------- #

    # fully_connected_graph = make_graph_fully_connected(graph)
    # print(get_polarization(fully_connected_graph))

    # --------------------------------------- #
    #              edge removals              #
    # --------------------------------------- #

    # edge_removals_driver(graph, name)


if __name__ == "__main__":
    main()
