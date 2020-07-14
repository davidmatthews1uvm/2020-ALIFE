import sqlite3
from time import time

import math
import numpy as np
import pandas as pd
from matplotlib import colors
from sklearn.linear_model import LinearRegression
from scipy.stats import spearmanr

import matplotlib.pyplot as plt
import matplotlib


# set matplotlib plot output font type to be valid for paper submission
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

database_file = "../data/database.db"


class RobotRecord(object):
    def __init__(self, id):
        self.id = id
        self.command_reinforcements_sum = {}
        self.command_reinforcements_total = {}

    def add_reinforcements(self, command, reinforcements):
        try:
            self.command_reinforcements_sum[command] += reinforcements
            self.command_reinforcements_total[command] += abs(reinforcements)
        except KeyError:
            self.command_reinforcements_sum[command] = reinforcements
            self.command_reinforcements_total[command] = abs(reinforcements)

    def get_top_commands(self, n, min_reinforcements = 1, extra=False, min_cmds=0):
        top_cmds = sorted(self.command_reinforcements_total.items(), key=lambda x: x[1], reverse=True)
        top_n_cmds = top_cmds[:n]
        if min_reinforcements > 1 and top_n_cmds[-1][1] < min_reinforcements:
            trim_idx = -1
            while trim_idx > -1 * len(top_n_cmds) and top_n_cmds[trim_idx][1] < min_reinforcements:
                trim_idx -= 1
            if trim_idx == -1 * len(top_n_cmds):
                return None
            top_n_cmds = top_n_cmds[:trim_idx]
        if len(top_n_cmds) < min_cmds:
            return None
        to_ret = np.empty(n)
        to_ret[:] = np.NaN
        to_ret[:len(top_n_cmds)] = sorted([self.get_normalized_reinforcements(cmd) for (cmd, count) in top_n_cmds])
        if extra:
            return (len(top_n_cmds), to_ret)
        else:
            return to_ret
    def get_commands(self):
        return [(cmd, self.get_normalized_reinforcements(cmd), self.command_reinforcements_total[cmd]) for cmd in self.command_reinforcements_total.keys()]

    def get_normalized_reinforcements(self, command):
        return self.command_reinforcements_sum[command]/self.command_reinforcements_total[command]

if __name__ == '__main__':
    # connect to the database + extract out relavent data to test if evolution is occuring.
    t0 = time()
    conn = sqlite3.connect(database_file)
    curr = conn.cursor()

    curr.execute("SELECT rowid, command, votes FROM UniqueCommands ORDER BY votes DESC")
    commands = curr.fetchall()
    num_commands = len(commands)
    curr.execute("select COUNT(*) from Robots")
    num_bots = curr.fetchall()[0][0]

    print("num_commands: %d, num_robots: %d"%(num_commands, num_bots))
    curr.execute(
        "SELECT Reinforcements.RobotId, UniqueCommands.command, UniqueCommands.rowid, Reinforcement, COUNT(Reinforcement)"
        " FROM Reinforcements JOIN Evaluations ON Reinforcements.EvaluationId = Evaluations.Id JOIN UniqueCommands on"
        " Evaluations.command = UniqueCommands.command GROUP BY"
        " Reinforcements.RobotId, UniqueCommands.command, Reinforcement")
    bot_evaluations = curr.fetchall()

    robots = {}
    for (robotId, command, rowId, reinforcement, count) in bot_evaluations:
        if robotId not in robots:
            robots[robotId] = RobotRecord(robotId)

        if reinforcement == "y":
            robots[robotId].add_reinforcements(command, count)
        elif reinforcement == "n":
            robots[robotId].add_reinforcements(command, -count)
        else:
            raise ValueError( "Invalid Reinforcement.")

    # compute a dense matrix of command, robot, evaluation triplets
    NUM_COMMANDS_TO_PLOT = 100
    MIN_REINFORCEMENTS = [1, 3]
    MIN_CMDS = 10
    for min_reinforcements in MIN_REINFORCEMENTS:
        print("Running with %d reinforcements per command robot pair"%min_reinforcements)
        robots_to_plot = []
        for robot in robots.values():
            tmp = robot.get_top_commands(NUM_COMMANDS_TO_PLOT, min_reinforcements=min_reinforcements, extra=True, min_cmds=MIN_CMDS)
            if tmp is not None:
                robots_to_plot.append((tmp,  robot))

        bots_matrix = np.zeros(shape=(len(robots_to_plot), NUM_COMMANDS_TO_PLOT))
        for n, data in enumerate(sorted(robots_to_plot, key=lambda x: x[0][0])):
            if n == len(robots_to_plot) -1:
                print("Robot id (%d) that had most commands evaluated:"%(data[1].id))
                robot_cmds = sorted(data[1].get_commands(), key=lambda x: x[1])
                for cmd in robot_cmds[:10]:
                    print(cmd[0], "&", cmd[1], "&", cmd[2],  "\\\\\\hline")
                for cmd in robot_cmds[-10:]:
                    print(cmd[0], "&", cmd[1], "&", cmd[2], "\\\\\\hline")
                # print(robot_cmds[:10], robot_cmds[-10:])
            bots_matrix[n] = data[0][1]
        fig, ax = plt.subplots(figsize=(6, 3))
        plt.imshow(bots_matrix.T, cmap="RdYlGn", aspect='auto')
        plt.colorbar(label="reinforcement")
        plt.xlabel("Robots")
        plt.ylabel("Commands")
        # plt.title("Reinforcements of commands for robots")
        plt.savefig("plots/RobotLearning_Sorted_%d_min_reinforcements.pdf"%min_reinforcements, bbox_inches='tight', pad_inches=0)
        plt.clf()

        # compute a sparse matrix of command, robot, evaluation triplets where each row is a command, and each column is a robot.
        MIN_COMMANDS_PER_ROBOT = [1, 40]
        for min_cmds_per_robot in MIN_COMMANDS_PER_ROBOT:
            robots_filtered = [r for r in robots.items() if len(r[1].command_reinforcements_total.values()) >= min_cmds_per_robot]

            commands_merged = set(command for r in robots_filtered for command in list(r[1].command_reinforcements_total.keys()))
            commands_idx = dict((cmd, idx) for idx, cmd in enumerate(commands_merged))
            robots_idx = dict((robot[0], idx) for idx, robot in enumerate(robots_filtered))

            bots_matrix_sparse = np.zeros(shape=(len(robots_filtered), len(commands_idx)))
            bots_matrix_sparse[:] = np.NaN
            for robotId, robot in robots_filtered:
                for (cmd, reinforcement, total_reinforcements) in robot.get_commands():
                    if total_reinforcements >= min_reinforcements:
                        bots_matrix_sparse[robots_idx[robotId], commands_idx[cmd]] = reinforcement

            print("robots:", len(robots_filtered), "cmd threshold:", min_cmds_per_robot, "ttl commands:" ,len(commands_idx))
            plt.imshow(bots_matrix_sparse.T, aspect=bots_matrix_sparse.shape[0] / bots_matrix_sparse.shape[1], cmap="RdYlGn")
            plt.colorbar(label="reinforcement")
            plt.xlabel("Robot Id")
            plt.ylabel("Command Id")
            plt.title("Reinforcements of commands for robots")
            plt.savefig("plots/RobotLearning_Sparse_min_%d_commands_per_robot_%d_min_reinforcements.pdf"%(min_cmds_per_robot, min_reinforcements), bbox_inches='tight', pad_inches=0)
            plt.clf()
