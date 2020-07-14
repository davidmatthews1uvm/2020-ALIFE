import random

from robot import ROBOT

import constants      as c
import localConstants as lc

class ROBOTS:

    def __init__(self,database,screen):

        self.Reset(database,screen)

    def Draw_Circles(self):

        for color in self.robots:

            self.robots[color].Draw_Circle()

    def Draw_Shadows(self):

        for color in self.robots:

            self.robots[color].Draw_Shadow()

    def Get_Max_Losses(self):

        return self.maxLosses

    def Get_Max_Wins(self):

        return self.maxWins

    def Get_Robot_Of_Color(self,color):

        return self.robots[color]

    def Print(self):

        for color in self.robots:

            self.robots[color].Print()

    def Reset(self,database,screen):

        numUndigestedReinforcements = database.Get_Num_Undigested_Reinforcements()

        self.robots = {}

        for color in c.colors:

            self.robots[color] = ROBOT(database,color,screen,numUndigestedReinforcements)

        self.Compute_Max_Wins_And_Losses()

        for color in c.colors:

            self.robots[color].Set_Position()

# ----------------- Private methods ------------------

    def Compute_Max_Wins_And_Losses(self):

        self.maxLosses = self.Find_Max_Losses()

        self.maxWins = self.Find_Max_Wins()

        for color in self.robots:

            self.robots[color].Set_Max_Wins(self.maxWins)

            self.robots[color].Set_Max_Losses(self.maxLosses)

    def Find_Max_Losses(self):

        maxLosses = -1

        for color in self.robots:

            if self.robots[color].Get_Losses() > maxLosses:

                maxLosses = self.robots[color].Get_Losses()

        return maxLosses + 2 # So that robots drawn to the far right can be seen 

    def Find_Max_Wins(self):

        maxWins = -1

        for color in self.robots:

            if self.robots[color].Get_Wins() > maxWins:

                maxWins = self.robots[color].Get_Wins()

        return maxWins + 2 # So that robots drawn at the top can be seen.
