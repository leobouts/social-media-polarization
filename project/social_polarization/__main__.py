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
    #      Graph Init                         #
    #      options: karate, polblogs, books   #
    #      ClintonTrump, GermanWings          #
    #      k: top-k edges to add              #
    # --------------------------------------- #

    # name = 'sxsw'
    # graph = load_graph(f'../datasets/{name}.gml')
    # print(get_polarization(graph))

    # --------------------------------------- #
    #     Heuristics experiment               #
    # --------------------------------------- #
    #                                         #
    #     Available Algorithms:               #
    #     1) Greedy                           #
    #     2) Greedy_Batch                     #
    #     3) Skip                             #
    #     4) Distance                         #
    #     5) Distance_Missing                 #
    #     6) Multiplication_Missing           #
    # --------------------------------------- #

    k = [1, 5, 10, 15, 20]

    algorithms = ["Distance_Missing", "Multiplication_Missing"]
    datasets = ["karate", "books"]

    heuristic_driver(k, datasets, algorithms)

    # --------------------------------------- #
    #     Fully connected for lemma 5.1       #
    # --------------------------------------- #

    # fully_connected_graph = make_graph_fully_connected(graph)
    # print(get_polarization(fully_connected_graph))

    # --------------------------------------- #
    #              edge removals              #
    # --------------------------------------- #

    # edge_removals_driver(graph, name)

    # costly brute force, polblogs dataset needs arround 200 hours to check, karate is ok.
    # find biggest and smallest decrease of nodes after adding an edge.
    # However this measures the state of the nodes and not the edges.
    # decreasing_dictionary = brute_force_opposing_views(graph, f'{name}.pickle', 0)
    # top_decrease, small_decrease = centralities(graph, decreasing_dictionary, 5)

    # visualize_graph(graph, top_decrease, small_decrease, 'addition')
    # print(top_decrease)


if __name__ == "__main__":
    main()
