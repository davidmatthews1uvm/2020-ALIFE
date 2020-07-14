import gc

import random

import sys

from visualizations.phylotree import PHYLOTREE
from visualizations.paretoFront import PARETO_FRONT
from visualizations.cumulativeYesVotes import CUMULATIVE_YES_VOTES
from visualizations.robotScoreboard import ROBOT_SCORE_BOARD
from visualizations.robotInfo import ROBOT_INFO
from visualizations.progress import PROGRESS
from visualizations.highScores import HIGH_SCORES

class VISUALIZATION:

    def __init__(self , database , positionsOfRobotsBeingSimulated , robots, oldRobotID=-1):

        self.database = database

        self.primaryBotPosition = -1

        self.primaryBotID = -1 

        self.secondaryBotPosition = -1

        self.secondaryBotID = -1

        self.robots = robots

        self.oldRobotID = oldRobotID

        self.Handle_Positions_Of_Robots_Being_Simulated( positionsOfRobotsBeingSimulated )

    def Save(self):

        # whichVisualizationToShow = random.randint(0,2)

        # paretoFront = PARETO_FRONT(self.database)

        # cyv = CUMULATIVE_YES_VOTES()

        self.Draw_Phylo_Tree()

        self.Draw_Robot_Info()

        # self.Draw_Pareto_Front()

        self.Draw_High_Scores_Table()

        #elif ( whichVisualizationToShow == 1 ):

        #    progress = PROGRESS(self.primaryBotPosition)

        #    progress.Draw()

        #    progress.Save()


        #elif ( whichVisualizationToShow == 2 and cyv.Sufficient_Conditions_For_Drawing() ):

        #    cyv.Collect_Data()

        #    cyv.Save()

        gc.collect()

    def Save_Empty_Image(self):

        phyloTree = PHYLOTREE()

        phyloTree.Draw_Empty()

# ----------------- Private methods --------------------------

    def Add_Primary_Robot(self, primaryBotPosition):

        self.primaryBotPosition = primaryBotPosition

        #-1 means the robot is old and needs to be fetched from the db (no longer in the robot list)
        if self.primaryBotPosition == -1:
            self.primaryBotID = self.oldRobotID
        else:
            self.primaryBotID = self.robots[primaryBotPosition].ID

    def Add_Secondary_Robot(self, secondaryBotPosition):

        self.secondaryBotPosition = secondaryBotPosition
        
        #-1 means the robot is old and needs to be fetched from the db (no longer in the robot list)
        if secondaryBotPosition == -1:
            self.secondaryBotID = self.oldRobotID
        else:
            self.secondaryBotID = self.robots[secondaryBotPosition].ID

    def Draw_High_Scores_Table(self):

        highScoresTable = HIGH_SCORES(self.database)

        highScoresTable.Draw()

        highScoresTable.Save()

    def Draw_Pareto_Front(self):
        
        paretoFront = PARETO_FRONT(self.database)

        if paretoFront.Sufficient_Conditions_For_Drawing() and self.database.Active_Users_Present():
        
            paretoFront.Draw( self.robots, self.primaryBotPosition )

        else:
            paretoFront.Draw_Empty()

    def Draw_Phylo_Tree(self):

        phyloTree = PHYLOTREE()

        #if self.database.Active_Users_Present():

        phyloTree.Draw( self.robots , self.primaryBotID , self.secondaryBotID )
        #else:
        #    phyloTree.Draw_Empty()

    def Draw_Robot_Info(self):

        robotInfo = ROBOT_INFO(self.primaryBotPosition)

        #if self.database.Active_Users_Present():

        robotInfo.Draw()
        #else:
        #    robotInfo.Draw_Empty()

        robotInfo.Save()

    def Handle_Positions_Of_Robots_Being_Simulated( self , positionsOfRobotsBeingSimulated):

        if ( len( positionsOfRobotsBeingSimulated ) >= 1 ):

            self.Add_Primary_Robot( positionsOfRobotsBeingSimulated[0] )

        if ( len( positionsOfRobotsBeingSimulated ) >= 2 ):

            self.Add_Secondary_Robot( positionsOfRobotsBeingSimulated[1] )
