from ages import get_robot_ages
import sqlite3

from time import time
import pickle
from tqdm import tqdm

import math
import numpy as np
import pandas as pd
from matplotlib import colors
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr
import scipy.spatial

import matplotlib.pyplot as plt
import matplotlib

import pygraphviz as pgv
import networkx as nx

# set matplotlib plot output font type to be valid for paper submission
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

database_file = "../data/database.db"
ignore_list_file = "ignore_list.txt"
def generate_single_ECDF(samples, ax=None, label=None, title="", xlabel="", ylabel="", xlog=False, color=None, reverse=False):
    """
    Plots an ECDF of samples
    :param samples: Samples to plot an ECDF of.
    :param ax: The Axis to plot on. Must not be None
    :param label: Any label to assign the line we are plotting.
    :return: None
    """
    assert ax is not None
    N = len(samples)
    X = sorted(samples, reverse=reverse)
    Y = [idx / N for idx in range(N)]
    ax.plot(X, Y, lw=3, label=label, alpha=1, c=color)
    ax.set_ylim((0, 1))
    ax.set_title(title, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_xlabel(xlabel, fontsize=15)

    if xlog:
        ax.set_xscale('log')


if __name__ == '__main__':
    # get list of ignore_listed commands.
    ignore_list = set(line.strip() for line in open(ignore_list_file, "r").readlines())

    # connect to the database + extract out relavent data to test if evolution is occuring.
    conn = sqlite3.connect(database_file)
    curr = conn.cursor()

    curr.execute("SELECT command, commandEncoding FROM UniqueCommands")
    commands_raw = curr.fetchall()
    num_commands = len(commands_raw)

    commands = sorted([(len(cmd.split(' ')), cmd.split(' '), cmd, np.mean(pickle.loads(cmd_raw), axis=0), pickle.loads(cmd_raw)) for cmd, cmd_raw in commands_raw if cmd not in ignore_list])
    commands_len_1 = [cmd for cmd in commands if cmd[0] == 1]

    print("There are %d commands in total."%len(commands))
    print("There are %d commands of length 1."%len(commands_len_1))

    commands = commands_len_1 # filter by single word commands.

    cmds_matrix = np.array([vec for (_, _, _, vec, _) in commands])

    cmds_norm_matrix = np.linalg.norm(cmds_matrix, axis=1)
    cmds_dot_matrix = np.dot(cmds_matrix, cmds_matrix.T)
    semantic_distances = []
    semantic_distances_dict = {}
    for c1, c2 in [(c1, c2) for c1 in range(len(commands)) for c2 in range(c1 + 1, len(commands))]:
        distance = abs(1- (cmds_dot_matrix[c1,c2]/(cmds_norm_matrix[c1]*cmds_norm_matrix[c2])))
        semantic_distances.append((commands[c1][2], commands[c2][2], distance))
        cmd_key = tuple(sorted((commands[c1][2], commands[c2][2])))
        semantic_distances_dict[cmd_key] = distance


    # load in behavioral similarity information.
    # for every evaluation, get every reinforcement pair.
    curr.execute(
        "SELECT e1.Id, e2.Id, e1.RobotId, r1.reinforcement, e2.RobotId, e1.command, r1.UserId, r2.UserId FROM Reinforcements r1 JOIN Reinforcements r2 on r1.Date = r2.Date AND r1.Id < r2.Id JOIN Evaluations e1 on r1.EvaluationId = e1.Id JOIN Evaluations e2 on r2.EvaluationId = e2.Id")
    data = curr.fetchall()

    df = pd.DataFrame(data,
                      columns=["e1.Id", "e2.Id", "robot1", "reinforcement1", "robot2", "command1", "user1", "user2"])
    df = df.drop(
        df[df["user1"] != df["user2"]].index)  # remove occurances where multiple users reinforce at the same time
    df = df.drop(df[df["robot1"] == df["robot2"]].index)  # eval 397, 398 of robot 20 is paired with robot 20.

    evals_by_robots = {}

    # bin evaluation pairs by robot ids
    for row in df.values:
        robot_1 = row[2]
        robot_2 = row[4]

        if robot_1 > robot_2:  # ensure robot 1 id is lower than robot 2 id
            robot_1 = robot_2
            robot_2 = row[2]

            # if robot ids are out of order, also need to switch ordering of row elements.
            row[2] = robot_1
            row[3] = 'y' if row[3] == 'n' else 'n'
            row[4] = robot_2

        try:
            s = evals_by_robots[(robot_1, robot_2)]
        except:
            s = []
            evals_by_robots[(robot_1, robot_2)] = s

        s.append(row)

    ages_df = get_robot_ages(curr)
    ages_dict = ages_df.T.to_dict('list')

    common_clades = sorted(dict(ages_df["clade"].value_counts()).items(), key = lambda x: x[1], reverse=True)

    NUM_CLADES = 7
    for n, (clade_id, count) in enumerate(common_clades[:NUM_CLADES]):
        print("Clade id %d with a rank of %d and %d robots" %(clade_id, n, count))
        filter_str = "MORPH_%d"%(clade_id)
        behavioral_similarity = {}
        stats = {"SameUser": 0, "DifferentUser": 0, "sameCmd": 0, "valid": 0, "young": 0, "old": 0, "mismatch": 0}
        for (robot_1, robot_2), eval_list in evals_by_robots.items():
            for e1 in range(len(eval_list)):
                for e2 in range(e1 + 1, len(eval_list)):
                    if eval_list[e1][-1] == eval_list[e2][-1]:
                        stats["SameUser"] += 1
                    else:
                        stats["DifferentUser"] += 1

                    cmd_1 = eval_list[e1][5]
                    cmd_2 = eval_list[e2][5]
                    if cmd_1 == cmd_2:
                        stats["sameCmd"] += 1
                        continue

                    if (ages_dict[eval_list[e1][2]][0] != ages_dict[eval_list[e1][4]][0] or ages_dict[eval_list[e1][4]][0] != clade_id):
                        stats["mismatch"] +=1
                        continue

                    cmd_key = tuple(sorted((cmd_1, cmd_2)))
                    agreement = 1 if eval_list[e1][3] == eval_list[e2][3] else 0 # did robot one either lose to robot two both times or win to it?

                    # is this the first time this command pair is appearing?
                    try:
                        s = behavioral_similarity[cmd_key]
                    except:
                        s = [0, 0]
                        behavioral_similarity[cmd_key] = s
                    s[0] += agreement
                    s[1] += 1
                    stats["valid"] +=1

        print("Statistics about which commands were filtered out or included.", stats)

        # How many reinforcements must a command pair get for inclusion?
        thresh = 1
        # keep track of why commands are not included.
        stats = {"keyError": 0, "thresh":0, "valid":0}
        semantic_behavioral_similarity_alignment = []

        for (cmd_1, cmd_2), (agreement, total) in behavioral_similarity.items():
            if total < thresh:
                stats["thresh"] +=1
                continue

            # Semantic similarity is not being computed for multi word commands and a few ignore_listed ones.
            try:
                sem_sim = semantic_distances_dict[(cmd_1, cmd_2)]
                semantic_behavioral_similarity_alignment.append([sem_sim, agreement/total])
                stats["valid"] += 1
            except KeyError as e:
                stats["keyError"] +=1

        semantic_behavioral_similarity_alignment = np.array(semantic_behavioral_similarity_alignment)
        if (semantic_behavioral_similarity_alignment.shape[0] < 2):
            print("Failed to compute spearmanr statistic. Not enough data points.")
            print(stats)
            continue

        X = semantic_behavioral_similarity_alignment[:,0]
        Y = 1 - semantic_behavioral_similarity_alignment[:,1]
        linreg = LinearRegression().fit(X.reshape(-1,1), Y.reshape(-1,1))

        spearmanr_res = spearmanr(X, Y)
        R, P = spearmanr_res
        P *= NUM_CLADES
        if P > 1: P = 1

        print("Filter: %s | Threshold %3d %s"%(filter_str, thresh, "R: %.3f P: %.5f"%spearmanr_res), stats)

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.scatter(X, Y, s=2)
        # ax.plot(X, linreg.predict(X.reshape(-1,1)), c="k")
        ax.set_xlabel("Semantic Distance")
        ax.set_ylabel("Behavioral Distance")
        ax.set_xlim([0.2, 1.1])
        ax.set_ylim([-0.1,1.1])

        if P > 0.05:
            ax.set_title("Clade %d %s"%(n, r"($r_s$=%.3f, $p > 0.05$)" % (R)), fontsize=18)
        else:
            ax.set_title("Clade %d %s"%(n, r"($r_s$=%.3f, $p = %.3E$)" % (R, P)), fontsize=18)
        # plt.savefig("plots/clade_%d.pdf"%(n), bbox_inches='tight', pad_inches=0)
        plt.savefig("plots/clade_rank_%d_id_%d.png"%(n, clade_id), bbox_inches='tight', pad_inches=0)
        plt.savefig("plots/clade_rank_%d_id_%d.pdf"%(n, clade_id), bbox_inches='tight', pad_inches=0)

        plt.clf()
        print("\n\n\n")


    # plot the clades
    for n, (clade_id, count) in enumerate(common_clades[:NUM_CLADES]):
        print("clade_id: %d"%clade_id, end="", flush=True)
        robots_of_interest = ages_df[ages_df["clade"] == clade_id]
        phyloTree = pgv.AGraph()
        for index, row in robots_of_interest.iterrows():
            node_fill_color = "lightgrey" if row.reinforcement <= 0 else "darkseagreen"
            phyloTree.add_node(row.name, label=str(int(row.name)), fixedsize=False, style='filled',
                               fillcolor=node_fill_color)
            if (int(row.parent_id) != -1):
                phyloTree.add_edge(int(row.parent_id), int(row.name))

        phyloTree.draw('plots/phylo_clade_rank_%d_id_%d.png' %(n, clade_id), prog='dot')
        print(" ... Done")

