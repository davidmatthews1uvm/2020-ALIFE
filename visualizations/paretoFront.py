import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import constants as c

class PARETO_FRONT:

    def __init__(self,database):

        self.database = database

    def Draw(self, robots, primaryBotPosition):
        plt.rcParams.update({'font.size': 22})
        fig, ax = plt.subplots(1)
        #fig.patch.set_facecolor('green')
        #fig.patch.set_alpha(0.0)

        self.Draw_Danger_Zones(ax, robots, self.database)
        self.Draw_Points(robots, self.database, primaryBotPosition)
        self.Resize_Figure(robots, self.database)
        self.Add_Labels(ax)

        plt.savefig('../visualizations/pF.png', facecolor=fig.get_facecolor(), transparent=True)
        os.system('mv ../visualizations/pF.png ../visualizations/paretoFront.png')
        fig.clf()

        del fig
        del ax

        plt.close()

    def Draw_Empty(self):
        plt.rcParams.update({'font.size': 22})
        fig, ax = plt.subplots(1)
        fig.clf()

        plt.savefig('../visualizations/pF.png', facecolor=fig.get_facecolor(), transparent=True)
        os.system('mv ../visualizations/pF.png ../visualizations/paretoFront.png')

        del fig
        del ax

        plt.close()

    def Sufficient_Conditions_For_Drawing(self):

        return self.database.Total_Positive_Reinforcements() > 0 and self.database.Total_Negative_Reinforcements() > 0

    # ------------ Private methods -------------------

    def Add_Labels(self, ax):

        if ( self.maxX > self.minX ):

            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax.set_xlabel('No votes',fontsize=22)
        ax.set_ylabel('Yes votes',fontsize=22)

        plt.tight_layout()

    def Draw_Danger_Zones(self, ax, robots, database):
        for aggressor in range(0, c.popSize):
            aggressorID = robots[aggressor].ID

            [ea, ya, na] = database.Get_Info_For_Robot(aggressorID)

            topLeftVertex = [na, ya]

            topRightVertex = [na+1000, ya]

            bottomRightVertex = [na+1000, -1]

            bottomLeftVertex = [na, -1]

            polygonVertices = [ topLeftVertex , topRightVertex , bottomRightVertex , bottomLeftVertex ]

            rect = patches.Polygon( polygonVertices , closed=True, color='k')

            ax.add_patch(rect)

    def Draw_Point(self, robots, database, botPosition, markerSize):
        botID = robots[botPosition].ID
        [e, y, n] = database.Get_Info_For_Robot(botID)

        nodeColor = c.colorNamesNoParens[botPosition]

        if (nodeColor == 'silver'):
            nodeColor = 'gray'

        elif (nodeColor == 'green'):
            nodeColor = 'darkgreen'

        elif (nodeColor == 'jade'):
            nodeColor = 'palegreen'

        plt.plot(n, y, 'bo', markerfacecolor=nodeColor, markeredgecolor='black', markersize=markerSize)

    def Draw_Points(self, robots, database, primaryBotPosition):
        if (primaryBotPosition > -1):
            self.Draw_Point(robots, database, primaryBotPosition, 48)

        for botPosition in range(0, c.popSize):
            if (botPosition != primaryBotPosition):
                self.Draw_Point(robots, database, botPosition, 24)

    def Resize_Figure(self, robots, database):
        self.minX = 1000
        self.maxX = -1000

        self.minY = 1000
        self.maxY = -1000

        for botPosition in range(0, c.popSize):
            botID = robots[botPosition].ID
            [e, y, n] = database.Get_Info_For_Robot(botID)

            if (self.minX > n):
                self.minX = n

            if (self.maxX < n):
                self.maxX = n

            if (self.minY > y):
                self.minY = y

            if (self.maxY < y):
                self.maxY = y

        xMargin = 0.1 * (self.maxX - self.minX) + 0.1
        yMargin = 0.1 * (self.maxY - self.minY) + 0.1
        plt.axis([self.minX - xMargin, self.maxX + xMargin, self.minY - yMargin, self.maxY + yMargin])
