import networkx as nx


def get_graph_type(g_type):

    graph = nx.Graph()

    if g_type == 'diamond':
        graph.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)])
        graph.name = 'diamond'
        return [graph, 4]
    elif g_type == 'paw':
        graph.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 3)])
        graph.name = 'paw'
        return [graph, 4]
    elif g_type == 'c4':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 3)])
        graph.name = 'c4'
        return [graph, 4]
    elif g_type == 'claw':
        graph.add_edges_from([(0, 1), (0, 2), (0, 3)])
        graph.name = 'claw'
        return [graph, 4]
    elif g_type == 'p4':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3)])
        graph.name = 'p4'
        return [graph, 4]
    # here start the 5-vertices graphs
    elif g_type == 'p3_union_2k1':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 3), (2, 4), (3, 4)])
        graph.name = 'p3_union_2k1'
        return [graph, 5]
    elif g_type == 'w4':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 3), (2, 4), (3, 4), (1, 4), (0, 4)])
        graph.name = 'w4'
        return [graph, 5]
    elif g_type == 'claw_union_k1':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 3), (3, 4), (0, 2), (1, 3)])
        graph.name = 'claw_union_k1'
        return [graph, 5]
    elif g_type == 'p2_union_p3':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 3), (3, 4), (1, 4), (0, 4)])
        graph.name = 'p2_union_p3'
        return [graph, 5]
    elif g_type == 'gem':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (1, 4), (0, 4), (2, 4)])
        graph.name = 'gem'
        return [graph, 5]
    elif g_type == 'k3_union2k1':
        graph.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (2, 3), (2, 4), (0, 3)])
        graph.name = 'k3_union2k1'
        return [graph, 5]
    elif g_type == 'k14':
        graph.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4)])
        graph.name = 'k14'
        return [graph, 5]
    elif g_type == 'butterfly':
        graph.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)])
        graph.name = 'butterfly'
        return [graph, 5]
    elif g_type == 'chair':
        graph.add_edges_from([(0, 1), (1, 2), (1, 3), (3, 4)])
        graph.name = 'chair'
        return [graph, 5]
    elif g_type == 'cofork':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (1, 4), (2, 4), ])
        graph.name = 'cofork'
        return [graph, 5]
    elif g_type == 'dart':
        graph.add_edges_from([(0, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), ])
        graph.name = 'dart'
        return [graph, 5]
    elif g_type == 'p5':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])
        graph.name = 'p5'
        return [graph, 5]
    elif g_type == 'house':
        graph.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)])
        graph.name = 'house'
        return [graph, 5]
    elif g_type == 'k23':
        graph.add_edges_from([(0, 1), (1, 2), (0, 4), (2, 4), (0, 3), (2, 3)])
        graph.name = 'k23'
        return [graph, 5]
    elif g_type == 'banner':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)])
        graph.name = 'banner'
        return [graph, 5]
    elif g_type == 'pdash':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 2)])
        graph.name = 'pdash'
        return [graph, 5]
    elif g_type == 'bull':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 1), (3, 4)])
        graph.name = 'bull'
        return [graph, 5]
    elif g_type == 'cricket':
        graph.add_edges_from([(0, 1), (1, 4), (1, 2), (2, 3), (1, 3)])
        graph.name = 'cricket'
        return [graph, 5]
    elif g_type == 'c5':
        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
        graph.name = 'c5'
        return [graph, 5]


def get_all_graphs():

    graphs = ['diamond', 'paw', 'c4', 'claw', 'p4', 'p3_union_2k1',
              'w4', 'claw_union_k1', 'p2_union_p3', 'gem', 'k3_union2k1', 'k14', 'butterfly', 'chair',
              'cofork', 'dart', 'p5', 'house', 'k23', 'banner', 'pdash', 'bull', 'cricket', 'c5']
    return graphs

