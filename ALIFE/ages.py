import sqlite3
from time import time

from datetime import datetime

import math
import numpy as np
import pandas as pd
from matplotlib import colors
from sklearn.linear_model import LinearRegression
from scipy.stats import  spearmanr

import matplotlib.gridspec as gridspec

import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable

# set matplotlib plot output font type to be valid for paper submission
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

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
    ax.set_title(title, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.set_xlabel(xlabel, fontsize=13)

    if xlog:
        ax.set_xscale('log')

class RobotRecord(object):
    """
    A robot class which serves to reconstruct the phylogenetic tree of robots from the complete list of robots.
    """
    def __init__(self, id, parent_id, lifespan):
        self.parent_id = parent_id
        self.id = id
        self.children = []
        self.age = 0
        self.clade = None
        self.yes_es = 0
        self.no_s = 0
        self.reinforcement = None
        self.lifespan = lifespan

    def __str__(self):
        return "Clade %4d | Robot %4d | Age %2d | Children [%s] | Yeses %3d | Nos %3d" % (self.clade, self.id, self.age, ",".join(["%4d"%id for id in self.children]), self.yes_es, self.no_s)

    def add_child(self, *child_ids):
        self.children += list(child_ids)

    def get_age_and_clade(self):
        return self.age, self.clade

    def set_age(self, robots):
        if self.parent_id == -1:
            self.age = 1
            self.clade = self.id
        else:
            parent_age, parent_clade = robots[self.parent_id].get_age_and_clade()
            assert parent_age != 0, "error in calculating parent age"
            assert parent_clade != None, "error in getting parent clade"

            self.clade = parent_clade
            self.age = parent_age + 1

    def get_data(self):
        # assert self.yes_es + self.no_s != 0, print(self)
        return (self.clade, self.id, self.parent_id, self.age, self.reinforcement, self.yes_es + self.no_s)

    def calc_reinforcement(self):
        self.reinforcement = (self.yes_es - self.no_s) / (self.yes_es + self.no_s)

    def set_yeses(self, yeses):
        self.yes_es = yeses
        self.calc_reinforcement()

    def set_nos(self, nos):
        self.no_s = nos
        self.calc_reinforcement()


def get_robot_ages(curr):
    t0 = time()
    curr.execute("SELECT Id, ParentId, BirthDate, DeathDate FROM ROBOTS")
    robots_raw = curr.fetchall()

    curr.execute(
        "Select RobotId, Reinforcement, COUNT(Reinforcement) from Reinforcements GROUP BY Reinforcement, RobotId")
    robot_reinforcements = sorted(curr.fetchall())

    t_query = time()
    print("Querying db took: %.2fs" % (t_query - t0))

    # build phylogenetic tree and compute genetic age of each robot.
    robots = [None] * len(robots_raw)

    for id, parent_id, birthdate, deathdate in robots_raw:
        lifespan = (datetime.fromisoformat(deathdate) - datetime.fromisoformat(birthdate)).total_seconds()
        robots[id] = RobotRecord(id, parent_id, lifespan)
        robots[id].set_age(robots)
        if parent_id > 0:
            robots[parent_id].add_child(id)

    for id, reinforcement, count in robot_reinforcements:
        if reinforcement == "y":
            robots[id].set_yeses(count)
        elif reinforcement == "n":
            robots[id].set_nos(count)
        else:
            raise ValueError("Invalid reinforcement")

    t_parse = time()
    print("Parsing took:  %.2fs" % (t_parse - t_query))

    # remove non-evaluated robots
    robots_df = pd.DataFrame([r.get_data() for r in robots], columns=["clade", "id", "parent_id","age", "reinforcement", "count"])
    print(
        "%d robots have never been evaluated. They likely were killed before they could be evaluated due to being in the population too long." %
        robots_df[robots_df["reinforcement"].isnull()].shape[0])
    robots_df.dropna(inplace=True)
    robots_df = robots_df.set_index("id")
    return robots_df

database_file = "../data/database.db"

def plot_heatmap_and_scatter(robots_df):

    ages = robots_df["age"].values.reshape(-1,1)
    reinforcements = robots_df["reinforcement"].values.reshape(-1,1)

    df_tmp = robots_df[["age", "reinforcement"]]
    max_reinforcements = df_tmp.groupby(df_tmp.columns.tolist(), as_index=False).size().max()


    color_bar_width = 0.05
    b_width = 1/(2 - color_bar_width)
    a_width = 1- b_width

    fig = plt.figure(figsize=(12, 12*a_width))

    gs0 = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[a_width, b_width], wspace=0.1)
    gs00 = gs0[0].subgridspec(1, 1)
    gs01 = gs0[1].subgridspec(1, 2, width_ratios=[1-color_bar_width, color_bar_width], wspace=0.05)

    f_ax1 = fig.add_subplot(gs00[0])
    f_ax2 = fig.add_subplot(gs01[0])
    f_ax3 = fig.add_subplot(gs01[1])
    axes = [f_ax1, f_ax2, f_ax3]

    heatmap = axes[1].hist2d(ages.flatten(), reinforcements.flatten(), bins=np.max(ages), cmap='Greys',
                             norm=colors.SymLogNorm(linthresh=1, linscale=1, vmin=0, vmax=max_reinforcements))
    cb = fig.colorbar(heatmap[-1], cax=axes[2], orientation="vertical")
    cb.set_label('Number of Reinforcements', fontsize=12)

    axes[1].set_xlim((0, 24.2))
    axes[1].set_ylim((-1.05, 1.05))

    linreg = LinearRegression().fit(ages, reinforcements)
    spearmanr_res = spearmanr(ages.flatten(), reinforcements.flatten())
    rval, pval = spearmanr_res

    axes[0].annotate(r"$r_s\; = %.3f$"%rval, xy = (20, 0.95))
    axes[0].annotate(r"$p\;= %.3f$"%pval, xy = (20, 0.85))

    axes[0].scatter(x=ages.flatten(), y=reinforcements.flatten(), s=1)
    axes[0].plot(ages, linreg.predict(ages), c="k")

    axes[0].set_xlim((0, 24.2))
    axes[0].set_ylim((-1.05, 1.05))
    axes[1].tick_params(labelleft=False)

    axes[0].set_xlabel("Generation", fontsize=18)
    axes[1].set_xlabel("Generation", fontsize=18)

    axes[0].set_ylabel("Average Reinforcement", fontsize=18)

    axes[0].set_title(r"$\bf{A}$.                            ", fontsize=24)
    axes[1].set_title(r"$\bf{B}$.                            ", fontsize=24)

    plt.subplots_adjust(wspace=0.3)
    plt.savefig("plots/Heatmap_with_lin_fit.png", bbox_inches='tight', pad_inches=0, dpi=300)
    plt.clf()

def plot_scatter(robots_df):

    ages = robots_df["age"].values.reshape(-1,1)
    reinforcements = robots_df["reinforcement"].values.reshape(-1,1)

    fig, ax = plt.subplots(figsize=(6, 3))

    linreg = LinearRegression().fit(ages, reinforcements)
    spearmanr_res = spearmanr(ages.flatten(), reinforcements.flatten())
    rval, pval = spearmanr_res

    ax.annotate(r"$r_s\; = %.3f$"%rval, xy = (17, 0.8), fontsize=18)
    if pval < 0.001:
        ax.annotate(r"$p\; \ll 0.001$", xy = (17, 0.55), fontsize=18)
    else:
        ax.annotate(r"$p\;= %.3f$"%pval, xy = (17, 0.55), fontsize=18)

    ax.scatter(x=ages.flatten(), y=reinforcements.flatten(), s=1)
    ax.plot(ages, linreg.predict(ages), c="k")

    ax.set_xlim((0, 24))
    ax.set_ylim((-1.05, 1.05))

    ax.set_xlabel("Generation", fontsize=18)

    ax.set_ylabel("Average Rein.", fontsize=18)

    plt.savefig("plots/Scatter_with_lin_fit.png", bbox_inches='tight', pad_inches=0, dpi=300)
    plt.savefig("plots/Scatter_with_lin_fit.pdf", bbox_inches='tight', pad_inches=0)
    plt.savefig("plots/Scatter_with_lin_fit.svg", bbox_inches='tight', pad_inches=0)
    plt.clf()

def plot_ecdfs(robots_df):
    ages = robots_df["age"].values.reshape(-1, 1)
    reinforcements = robots_df["reinforcement"].values.reshape(-1, 1)

    # plot a heatmap of where the most common reinforcement / age pairs are occuring.

    # plt.show()
    # exit(1)
    # bin the robots based on age and plot a ECDF of each age group's reinforcement distribution.
    # notice that older robots follow the same rough distribution but have slightly higher probability of being considered good.
    # GROUPS = [1, 3, 5] # [1,2,3,4,5,6]
    GROUPS = [3, 5]
    N_GROUPS = len(GROUPS)
    fig, axes = plt.subplots(ncols=1,  nrows=N_GROUPS, figsize=(6, 3.5))


    for j in range(N_GROUPS):
        ax = axes[j]
        percentiles = GROUPS[j]
        percentile = 100 / percentiles

        for i in range(percentiles):
            min = np.percentile(ages.flatten(), percentile * i)
            max = np.percentile(ages.flatten(), percentile * (i + 1))
            if min == max:
                min -= 1
            reinforcements = sorted(robots_df[(robots_df["age"] <= max) & (robots_df["age"] > min)]["reinforcement"].values)

            generate_single_ECDF(reinforcements, ax=ax, reverse=True, label="[%d, %d)" % ( min, max))
        ax.legend()

        if N_GROUPS != 1:
            ax.annotate("%s"%("ABC"[j]), xy=(-0.95, 0.7), fontsize=18)
        ax.set_ylabel(r"$P(Rein.)_{>x}$")

        if j == N_GROUPS -1:
            ax.set_xlabel("Average Reinforcement")
        else:
            ax.xaxis.set_ticklabels([])
    plt.savefig("plots/ECDF_Age_vs_Reinforcement.svg", bbox_inches='tight', pad_inches=0) # save as svg and manually convert to pdf
    plt.savefig("plots/ECDF_Age_vs_Reinforcement.png", bbox_inches='tight', pad_inches=0, dpi=300) # save as svg and manually convert to pdf
    plt.savefig("plots/ECDF_Age_vs_Reinforcement.pdf", bbox_inches='tight', pad_inches=0) # save as svg and manually convert to pdf
    plt.clf()


if __name__ == '__main__':
    # connect to the database + extract out relavent data to test if evolution is occuring.
    t0 = time()
    conn = sqlite3.connect(database_file)
    curr = conn.cursor()

    robots_df = get_robot_ages(curr)
    plot_heatmap_and_scatter(robots_df)
    plot_scatter(robots_df)
    plot_ecdfs(robots_df)

    # curr.execute("SELECT u1.Id, count(u1.Id) From Users u1 JOIN Reinforcements r1 on u1.Id = r1.UserId JOIN Reinforcements r2 on r1.Date = r2.Date where r1.Id < r2.Id GROUP BY u1.Id ORDER BY COUNT(u1.Id)")
    # curr.execute("SELECT u1.Id, count(u1.Id) From Users u1 JOIN Reinforcements r1 on u1.Id = r1.UserId JOIN Reinforcements r2 on r1.Date = r2.Date where r1.Id < r2.Id GROUP BY u1.Id ORDER BY COUNT(u1.Id)")

    # number of evals per user is somewhat of a power-law distribution.
    # evals_per_user = np.array(curr.fetchall())[:,1]
    # fig, ax = plt.subplots()
    # generate_single_ECDF(evals_per_user, ax=ax, xlog=True)
    # plt.show()
