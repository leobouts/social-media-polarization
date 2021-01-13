from __visualize__ import vis_graphs_heuristics
import pickle
import time
import os
import re

def open_pickles_for_adjusting_visualization_manually(k, dataset_name, experiment_time):
    with open(f"../pickles/{dataset_name}/{experiment_time}/{dataset_name}_decreases_checked_pol", 'rb') as fp:
        decreases_checked = pickle.load(fp)

    with open(f"../pickles/{dataset_name}/{experiment_time}/{dataset_name}_labels_checked_pol", 'rb') as fp:
        labels_checked = pickle.load(fp)

    k_copy = k.copy()
    k_copy.insert(0, 0)

    vis_graphs_heuristics(k_copy,
                          decreases_checked,
                          labels_checked,
                          f"{dataset_name} Polarization Decrease",
                          "Number of Edges Added",
                          "π(z)",
                          0)


def open_pickle(path):
    with open(path, 'rb') as fp:
        info = pickle.load(fp)

    return info


def save_data_to_pickle(data_to_write, atr_list, ds, experiment_comment):
    experiment_time = (time.asctime(time.localtime(time.time())))

    try:
        os.mkdir(f'../pickles/{ds}/{experiment_time} {experiment_comment}')

    except OSError:
        print("Creation of the directory %s failed" % f'../pickles/{ds}/{experiment_time}')

    for i in range(len(data_to_write)):
        with open(f"../pickles/{ds}/{experiment_time}/{ds}_{atr_list[i]}", 'wb') as handle:
            pickle.dump(data_to_write[i], handle, protocol=pickle.HIGHEST_PROTOCOL)
