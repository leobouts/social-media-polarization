from __visualize__ import vis_graphs_heuristics
import pickle


def open_pickles_for_adjusting_visualization_manually(k, dataset_name):
    with open(f"../pickles/{dataset_name}/{dataset_name}_decreases_checked_pol", 'rb') as fp:
        decreases_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{dataset_name}_labels_checked_pol", 'rb') as fp:
        labels_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{dataset_name}_times_checked", 'rb') as fp:
        times_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{dataset_name}_labels_checked_time", 'rb') as fp:
        time_labels_checked = pickle.load(fp)

    k_copy = k.copy()
    k_copy.insert(0, 0)

    vis_graphs_heuristics(k_copy,
                          decreases_checked,
                          labels_checked,
                          f"{dataset_name} Polarization Decrease",
                          "Number of Edges Added",
                          "π(z)",
                          0)

    vis_graphs_heuristics(k,
                          times_checked,
                          time_labels_checked,
                          f"{dataset_name} Time Elapsed",
                          "Number of Edges Added",
                          "Seconds",
                          1)


def open_info_pickle(dataset_name):
    with open(f"../pickles/{dataset_name}/{dataset_name}_info", 'rb') as fp:
        info = pickle.load(fp)

    return info
