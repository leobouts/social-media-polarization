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

    # name = 'sxsw'
    # graph = load_graph(f'../datasets/{name}.gml')
    # print(get_polarization(graph))

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

    k = [1, 5, 10, 15, 20]

    algorithms = ["Distance"]
    datasets = ["polblogs"]
    heuristic_driver(k, datasets, algorithms)

    # heuristic_driver(k, ["sxsw", "ClintonTrump", "GermanWings"], ["Distance"])
    # heuristic_driver(k, ["beefban", "polblogs"], ["Skip", "Distance"])

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
