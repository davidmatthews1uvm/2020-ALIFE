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
from scipy.stats import  spearmanr
import scipy.spatial

import matplotlib.pyplot as plt
import matplotlib

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
    for c1, c2 in tqdm([(c1, c2) for c1 in range(len(commands)) for c2 in range(c1 + 1, len(commands))]):
        distance = abs(1- (cmds_dot_matrix[c1,c2]/(cmds_norm_matrix[c1]*cmds_norm_matrix[c2])))
        semantic_distances.append((commands[c1][2], commands[c2][2], distance))
        cmd_key = tuple(sorted((commands[c1][2], commands[c2][2])))
        semantic_distances_dict[cmd_key] = distance

    # get top N commands
    # for each pair, compute the semantic distance and print the most and least aligned pairs.
    TOP_N_MOST_REINFORCED_COMMANDS = 550
    curr.execute("Select command, COUNT(command) from Reinforcements r JOIN Evaluations e on r.EvaluationId = e.Id GROUP BY command ORDER BY COUNT(command) DESC limit ?", (TOP_N_MOST_REINFORCED_COMMANDS,))
    top_commands = [(cmd, rank) for rank, (cmd, reinforcement_count) in enumerate(curr.fetchall()) if len(cmd.split(' ')) == 1 and cmd not in ignore_list]
    top_commands_distances = []
    top_commands = top_commands[:300]

    for c1, c2 in tqdm([(c1, c2) for c1 in range(len(top_commands)) for c2 in range(c1 + 1, len(top_commands))]):
        cmd1, rank1 = top_commands[c1]
        cmd2, rank2 = top_commands[c2]
        top_commands_distances.append((cmd1, rank1, cmd2, rank2, semantic_distances_dict[(tuple(sorted((cmd1, cmd2))))]))

    top_commands_distances = sorted(top_commands_distances, key=lambda x: x[4])

    for c1, r1, c2, r2, dist in top_commands_distances[:10]:
        print("%.2f & %s & %2d & %s & %2d \\\\\hline"%(dist, c1, r1, c2, r2))
    print("\\hline")
    for c1, r1, c2, r2, dist in top_commands_distances[-10:]:
        print("%.2f & %s & %2d & %s & %2d \\\\\hline"%(dist, c1, r1, c2, r2))

    exit(1)
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
    print("The most common clades are:")
    print(common_clades[:10])

    # print out age distribution stats
    print("Percentile vs. age of robots")
    for i in range(0, 100, 10):
        print("%2.d%%: "%i, np.percentile(ages_df.age.values, i))
    age_thresh = np.percentile(ages_df["age"].values, 50)
    NO_FILTER = 0
    YOUNG = 1
    OLD = 2
    MORPH = 3
    MORPH_CLADE = common_clades[4][0]
    SAME_CLADE_PAIRS = 4
    # for each robot pair, there is a list of evaluations that both robots were in.
    # consider each pair of these evaluations.
    # where commands and users are different, update behavioral distance calculations.
    for MODE in [NO_FILTER, YOUNG, OLD, MORPH, SAME_CLADE_PAIRS]:
        filter_str = ""
        if MODE == NO_FILTER:
            filter_str = "NO_FILTER"
        elif MODE == YOUNG:
            filter_str = "YOUNG"
        elif MODE == OLD:
            filter_str = "OLD"
        elif MODE == MORPH:
            filter_str = "MORPH_%d"%(MORPH_CLADE)
        elif MODE == SAME_CLADE_PAIRS:
            filter_str = "SAME_CLADE_PAIRS"
        behavioral_similarity = {}
        stats = {"SameUser": 0, "DifferentUser": 0, "sameCmd": 0, "valid": 0, "young": 0, "old": 0, "mismatch": 0}
        for (robot_1, robot_2), eval_list in evals_by_robots.items():
            for e1 in range(len(eval_list)):
                for e2 in range(e1 + 1, len(eval_list)):
                    if False: #eval_list[e1][-1] == eval_list[e2][-1]:
                        stats["SameUser"] += 1
                    else:
                        stats["DifferentUser"] += 1
                        cmd_1 = eval_list[e1][5]
                        cmd_2 = eval_list[e2][5]
                        if cmd_1 == cmd_2:
                            stats["sameCmd"] += 1
                        else:
                            if MODE == YOUNG or MODE == OLD: # should we bin by ages?
                                if ages_dict[eval_list[e1][2]][1] <= age_thresh: # is the first robot young?
                                    if ages_dict[eval_list[e1][4]][1] <= age_thresh: # is the second robot young?
                                        stats["young"] +=1
                                        if MODE != YOUNG: continue
                                    else: # the first robot is young and the second is not
                                        stats["mismatch"] += 1
                                        continue
                                elif ages_dict[eval_list[e1][4]][1] > age_thresh: # The first robot is old. Is the second one?
                                    stats["old"] += 1
                                    if MODE != OLD: continue
                                else: # the first robot is old and the second one is young.
                                    stats["mismatch"] += 1
                                    continue
                            if MODE == MORPH and  (ages_dict[eval_list[e1][2]][0] != ages_dict[eval_list[e1][4]][0] or ages_dict[eval_list[e1][4]][0] != MORPH_CLADE):
                                stats["mismatch"] +=1
                                continue
                            if MODE == SAME_CLADE_PAIRS and ages_dict[eval_list[e1][2]][0] != ages_dict[eval_list[e1][4]][0]:
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

        # thresh_invert determines if we are picking commands with a behavioral_similarity that includes at least or no more than
        # N reinforcements.
        for thresh_invert in [False]: #[False, True]:
            # How many reinforcements must a command pair get for inclusion?
            for thresh in range(0, 50, 2):
                # keep track of why commands are not included.
                stats = {"keyError": 0, "thresh":0, "valid":0}
                semantic_behavioral_similarity_alignment = []

                for (cmd_1, cmd_2), (agreement, total) in behavioral_similarity.items():
                    if not thresh_invert and total < thresh: stats["thresh"] +=1; continue
                    if thresh_invert and total > thresh: stats["thresh"] +=1; continue

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

                print("Filter: %s | Threshold %3d %s"%(filter_str, thresh, "R: %.3f P: %.5f"%spearmanr_res), stats)

                plt.scatter(X, Y, s=2)
                plt.plot(X, linreg.predict(X.reshape(-1,1)), c="k")
                plt.xlabel("Semantic Similarity")
                plt.ylabel("Motoric Similarity")
                plt.xlim([0,1.25])
                plt.ylim([0,1.1])

                plt.title("Sem Motor Alignment Thresh of %d Inverted %d %s"%(thresh, thresh_invert, r"\n($r_s$=%.3f, P=%.3f)" % spearmanr_res), fontsize=18)
                plt.savefig("plots/SemanticMotoricAlignment_%s_Thresh_%d_R_%.3f.pdf"%(filter_str, thresh, spearmanr_res[0]), bbox_inches='tight', pad_inches=0)

                plt.clf()