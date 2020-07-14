from ages import get_robot_ages
import sqlite3

from time import time
import pickle
from tqdm import tqdm

import math
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr
import scipy.spatial

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors
import matplotlib.gridspec as gridspec


# set matplotlib plot output font type to be valid for paper submission
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

database_file = "../data/database.db"
ignore_list_file = "ignore_list.txt"

def load_semantic_distances_dict(curr):
    # get list of ignore_listed commands.
    ignore_list = set(line.strip() for line in open(ignore_list_file, "r").readlines())

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

    return semantic_distances_dict

def load_evals_by_robot(curr):

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
    return evals_by_robots

def get_behavioral_sim(evals_by_robots, ages_dict):
    behavioral_similarity = {}
    behavioral_sim_ages = {}
    stats = {"SameUser": 0, "DifferentUser": 0, "sameCmd": 0, "valid": 0, "young": 0, "old": 0, "mismatch": 0}
    for (robot_1, robot_2), eval_list in evals_by_robots.items():
        for e1 in range(len(eval_list)):
            for e2 in range(e1 + 1, len(eval_list)):
                if eval_list[e1][-1] == eval_list[e2][-1]:
                    stats["SameUser"] += 1
                    continue
                else:
                    stats["DifferentUser"] += 1
                cmd_1 = eval_list[e1][5]
                cmd_2 = eval_list[e2][5]
                if cmd_1 == cmd_2:
                    stats["sameCmd"] += 1
                    continue

                cmd_key = tuple(sorted((cmd_1, cmd_2)))
                agreement = 1 if eval_list[e1][3] == eval_list[e2][
                    3] else 0  # did robot one either lose to robot two both times or win to it?

                # is either robot old.
                AGE_THRESH = 1

                if ages_dict[eval_list[e1][4]][3] > AGE_THRESH and  ages_dict[eval_list[e1][6]][3] > AGE_THRESH:
                    try:
                        behavioral_sim_ages[cmd_key] += 1
                    except:
                        behavioral_sim_ages[cmd_key] = 1

                # is this the first time this command pair is appearing?
                try:
                    s = behavioral_similarity[cmd_key]

                except:
                    s = [0, 0]
                    behavioral_similarity[cmd_key] = s

                s[0] += agreement
                s[1] += 1
                stats["valid"] += 1

    print("Statistics about which commands were filtered out or included.", stats)
    return behavioral_similarity, behavioral_sim_ages

def get_sem_behavioral_alignement(thresh, sem_dist_dict, behavioral_sim, behavioral_sim_ages):
    # keep track of why commands are not included.
    stats = {"keyError": 0, "thresh": 0, "valid": 0, "young":0, "old":0}
    semantic_behavioral_similarity_alignment = []


    for (cmd_1, cmd_2), (agreement, total) in behavioral_sim.items():
        if total < thresh:
            stats["thresh"] += 1
            continue
        try:
            old = behavioral_sim_ages[(cmd_1, cmd_2)]
        except:
            old = 0
        young = total - old
        stats["young"] += young
        stats["old"] += old

        # Semantic similarity is not being computed for multi word commands and a few ignore_listed ones.
        try:
            sem_sim = sem_dist_dict[(cmd_1, cmd_2)]
            semantic_behavioral_similarity_alignment.append([sem_sim, agreement / total])
            stats["valid"] += 1
        except KeyError as e:
            stats["keyError"] += 1

    return (semantic_behavioral_similarity_alignment, stats)

def plot_scatter(ax, X, Y, rval, pval, thresh, label_y = True):
    linreg = LinearRegression().fit(X.reshape(-1, 1), Y.reshape(-1, 1))
    ax.scatter(X, Y, s=2)
    ax.plot(X, linreg.predict(X.reshape(-1, 1)), c="k")
    ax.set_xlabel("Semantic Distance")
    if label_y:
        ax.set_ylabel("Behavioral Distance ")
    else:
        ax.yaxis.set_ticklabels([])
    ax.set_xlim([0, 1.25])
    ax.set_ylim([0, 1.1])

    ax.annotate(r"$r_s\; = %.3f$"%rval, xy = (0.05, 1.005))
    ax.annotate(r"$p\;= %.3f$"%pval, xy = (0.05, 0.9))
    ax.annotate(r"$\theta\;= %2d$" % thresh, xy=(0.8, 1.005))

def label(ax, rect, offsetx, offsety):
    height = rect.get_height()
    ax.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width()/2, height),
                xytext=(offsetx, offsety),
                arrowprops=dict(facecolor='black', width = 0.005, headwidth=5, headlength=3, color="grey"),
                textcoords="offset points",
                ha='center', va='bottom',
                rotation="horizontal", color = "C0")

def plot_bar_plot(ax, thresh_dat, annotation = None):
    ax.set_xlabel("Reinforcements Threshold")

    r_vals, p_vals, num_obs = zip(*threshold_data)

    # plot the observation counts
    ax_invs = ax.twinx()
    ax_invs.set_yticks([])
    rects = ax_invs.bar(range(1, len(thresh_dat)+1), num_obs, label="Number of observations")

    # observation labels
    label(ax_invs, rects[0], 60, -7)
    label(ax_invs, rects[10], 30, 30)
    label(ax_invs, rects[20], 10, 20)
    label(ax_invs, rects[-1], -30, 15)

    # pearson R correlation
    ax.plot(r_vals, c='k')
    ax.set_ylabel(r"Spearman $r_s$ correlation")

    # pvals
    p_vals = np.array(p_vals)
    p_vals *= len(p_vals) # bon-ferroni correction.
    axr = ax.twinx()  # instantiate a second axes that shares the same x-axis
    axr.set_ylim(0, 0.5)
    axr.set_ylabel("P Value", color = "red")
    axr.tick_params(axis='y', labelcolor="red")
    axr.plot(p_vals, c='r')

    if annotation is not None:
        ax_invs.annotate(annotation, xy=(30, 3000), fontsize=18)


    axr.set_zorder(ax_invs.get_zorder() + 1)
    axr.patch.set_visible(False)
    ax.set_zorder(ax_invs.get_zorder() + 2)
    ax.patch.set_visible(False)


if __name__ == '__main__':

    # connect to the database + extract out relavent data to test if evolution is occuring.
    conn = sqlite3.connect(database_file)
    curr = conn.cursor()

    semantic_distances_dict = load_semantic_distances_dict(curr)
    evals_by_robots = load_evals_by_robot(curr)
    ages_df = get_robot_ages(curr)

    ages_dict = ages_df.T.to_dict('list')

    behavioral_similarity, behavioral_sim_ages = get_behavioral_sim(evals_by_robots, ages_dict)

    fig = plt.figure(figsize=(9, 2))
    gs0 = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[0.65, 0.35], wspace=0.3)
    gs00 = gs0[0].subgridspec(1,2)
    gs01 = gs0[1].subgridspec(1,1)

    f_ax1 = fig.add_subplot(gs00[0])
    f_ax2 = fig.add_subplot(gs00[1])
    f_ax3 = fig.add_subplot(gs01[0])
    axes = [f_ax1, f_ax2, f_ax3]

    NUM_THRESHES = 40
    threshold_data = [None] * NUM_THRESHES # (Rval, pval, num observations)

    # How many reinforcements must a command pair get for inclusion?
    for thresh in range(1, NUM_THRESHES + 1):
        semantic_behavioral_similarity_alignment, stats = get_sem_behavioral_alignement(thresh, semantic_distances_dict, behavioral_similarity, behavioral_sim_ages)

        semantic_behavioral_similarity_alignment = np.array(semantic_behavioral_similarity_alignment)
        if (semantic_behavioral_similarity_alignment.shape[0] < 2):
            print("Failed to compute spearman statistic. Not enough data points.")
            continue

        X = semantic_behavioral_similarity_alignment[:,0]
        Y = 1 - semantic_behavioral_similarity_alignment[:,1]

        spearmanr_res = spearmanr(X, Y)
        rval, pval = spearmanr_res
        pval *= NUM_THRESHES # apply Bonferroni family wise error rate correction.
        pval = min(pval, 1)
        threshold_data[thresh - 1] = (*spearmanr_res, stats["valid"])

        if thresh == 1:
            plot_scatter(axes[0], X, Y, rval, pval, thresh)
        elif thresh== 34:
            plot_scatter(axes[1], X, Y, rval, pval, thresh, label_y=False)

        print("Threshold %3d %s"%( thresh, "R: %.3f P: %.5f"%spearmanr_res), stats)

    plot_bar_plot(axes[2], threshold_data, annotation="C")
    axes[0].annotate("%s" % ("A"), xy=(0.1, 0.7), fontsize=18)
    axes[1].annotate("%s" % ("B"), xy=(0.1, 0.7), fontsize=18)
    # fig.suptitle("Semantic Motoric Alignment", fontsize=18)
    plt.savefig("plots/SemanticMotoricAlignment.pdf", bbox_inches='tight', pad_inches=0)
    plt.savefig("plots/SemanticMotoricAlignment.png", bbox_inches='tight', pad_inches=0, dpi=300)