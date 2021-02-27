from __visualize__ import vis_graphs_heuristics, final_plot, vis_graphs_heuristics_bar
import pickle
import time
import os
import pandas as pd


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
    experiment_time = experiment_time.replace("/", ".")
    try:
        os.mkdir(f'../pickles/{ds}/{experiment_time} {experiment_comment}')

    except OSError:
        print("Creation of the directory %s failed" % f'../pickles/{ds}/{experiment_time}')

    for i in range(len(data_to_write)):
        with open(f"../pickles/{ds}/{experiment_time} {experiment_comment}/{ds}_{atr_list[i]}", 'wb') as handle:
            pickle.dump(data_to_write[i], handle, protocol=pickle.HIGHEST_PROTOCOL)


def open_pickles_for_final(k, dataset_names, algos):

    """
    note to self: when doing experiments for the larger datasets please keep the same order with the small
    because on the larger you will not use the greedy algorithms but the order matters when you will want
    to create this final plot here to be correct.
    :param k:
    :param dataset_names:
    :param algos:
    :return:
    """

    lst_of_df = []
    k_copy = k
    k_copy.insert(0, 0)

    # num_of_edges = [
    #     [0, 10, 20, 30, 40],
    #     [0, 25, 50, 75, 100],
    #     [0, 200, 400, 600, 800],
    #     [0, 400, 800, 1200, 1600],
    #     [0, 700, 1400, 2100, 2800],
    #     [0, 500, 1000, 1500, 2000]
    # ]

    for i,dataset_name in enumerate(dataset_names):

        with open(f"../pickles/final/{dataset_name}_decreases_checked_pol", 'rb') as fp:

            decreases_checked = pickle.load(fp)

        with open(f"../pickles/final/{dataset_name}_labels_checked_pol", 'rb') as fp:
            labels_checked = pickle.load(fp)

        #for same edges in all graphs add k_copy instead in columns
        #df = pd.DataFrame(decreases_checked, columns=num_of_edges[i])

        df = pd.DataFrame(decreases_checked, columns=k_copy)
        lst_of_df.append(df)

    final_plot(lst_of_df, dataset_names, k_copy, algos)
