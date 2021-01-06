from __format_datasets__ import convert_dataset_to_gml, get_nodes_and_values_from_nx_to_txt
from __load_graph_data__ import load_graph


def convert_datasets_driver():
    base_data_dir = "/Users/leonidas/desktop/February 21/thesis/Data/"

    communities_values = ["Germanwings/communities_germanwings",
                          "Beefban/communities_beefban",
                          "sxsw/communities_sxsw",
                          "Elections/ClintonTrumpCommunities3000"]

    communities_connections = ["Germanwings/germanwings_followers_network_part_largest_CC",
                               "Beefban/beefban_followers_network_part_largest_CC",
                               "sxsw/sxsw_followers_network_part_largest_CC",
                               "Elections/ClintonTrumpEdges3000"]

    names_to_save = ["GermanWings.gml", "beefban.gml", "sxsw.gml", "ClintonTrump.gml"]

    for i in range(len(communities_values)):
        val = base_data_dir + communities_values[i]
        ed = base_data_dir + communities_connections[i]
        convert_dataset_to_gml(val, ed, names_to_save[i])


def convert_networkx_to_txt_for_embeddings_driver():
    datasets = ['karate', 'polblogs', 'books', 'ClintonTrump', 'GermanWings', 'sxsw', 'beefban']

    for ds_name in datasets:
        graph = load_graph(f'../datasets/{ds_name}.gml')
        get_nodes_and_values_from_nx_to_txt(graph, ds_name)