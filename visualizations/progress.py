from datetime import datetime

import math

import matplotlib.pyplot as plt

import random



from database.database import DATABASE

import constants as c

class PROGRESS:

    def __init__(self,primaryRobotIndex):

        self.primaryRobotIndex = primaryRobotIndex

        self.db = DATABASE()

        self.highestBIndex = -1

        self.experimentStartTime = self.Compute_Experiment_Start_Time()

    def Draw(self):

        self.Prep_Drawing()

        self.robots = self.db.Get_Robots()

        for robot in self.robots:

            self.Handle_Robot(robot)

        self.Draw_Current_Robot()

        self.Annotate_Figure()

    def Save(self):

        plt.savefig('test.png', facecolor=self.fig.get_facecolor(), transparent=True)

        plt.close()

# ------------- Private methods ----------------

    def Add_Robot_Creation_Date(self,robot):

        robotCreationDateAsString = self.db.From_Robot_Record_Get_Creation_Date(robot)

        robotCreationDate = datetime.strptime(robotCreationDateAsString, '%Y-%m-%d %H:%M:%S')

        totalSecondsElapsed = int((robotCreationDate - self.experimentStartTime).total_seconds())

        self.xCoordinates.append( totalSecondsElapsed )

        self.yCoordinates.append( 0 + 0.01 * self.robotColorIndex )

    def Annotate_Figure(self):
        handles, labels = self.ax.get_legend_handles_labels()

        xTicks = [0, self.Seconds_Elapsed_So_Far()]
        xTickLabels = ['Start', 'Now']
        plt.xticks(xTicks, xTickLabels,fontsize=22,horizontalalignment='left')

        yint = range(0, math.ceil(self.highestBIndex)+1)

        plt.yticks(yint)

        plt.ylabel('Scores.',fontsize=22)

        plt.tight_layout()

    def Compute_Experiment_Start_Time(self):

        firstRobot = self.db.Get_First_Robot()

        firstRobotCreationDateAsString = self.db.From_Robot_Record_Get_Creation_Date(firstRobot)

        return datetime.strptime(firstRobotCreationDateAsString, '%Y-%m-%d %H:%M:%S')

    def Draw_Current_Robot(self):

        currentRobot = self.db.Get_Living_Robot_At_Position( self.primaryRobotIndex )

        currentRobotID = self.db.From_Robot_Record_Get_ID(currentRobot)

        x = self.Seconds_Elapsed_So_Far()

        y = self.db.Get_B_Index_For_Robot(currentRobotID) + 0.01 * self.primaryRobotIndex

        dotColor = c.colorRGBs[self.primaryRobotIndex]

        plt.plot( x , y , 'ko' , markeredgecolor = 'black' , markerfacecolor = dotColor , markersize = 24 )

    def Draw_Horizontal_Line_To_Right_Of_Plot(self):

            x = self.Seconds_Elapsed_So_Far()

            y = self.yCoordinates[-1]

            self.xCoordinates.append(x)

            self.yCoordinates.append(y)
 
    def Draw_Robots_BIndices(self):

        if self.xCoordinates == []:

            return

        lineColor = c.colorRGBs[ self.robotColorIndex ]

        if lineColor == [1,1,1]:

            lineColor = [0,0,0]

        if self.db.Robot_Is_Alive(self.robotID):

            self.Draw_Horizontal_Line_To_Right_Of_Plot()

        plt.plot( self.xCoordinates , self.yCoordinates , color = lineColor , linewidth = 2 )

    def Handle_Reinforcement(self):

        signal = self.db.From_Reinforcement_Record_Get_Signal(self.reinforcement)

        if signal == 'n':

            return

        timeOfReinforcementAsAString = self.db.From_Reinforcement_Record_Get_Time(self.reinforcement)

        BIndex = self.db.Get_B_Index_For_Robot_At_Time(self.robotID,timeOfReinforcementAsAString)

        if ( BIndex > self.highestBIndex ):

            self.highestBIndex = BIndex

        timeOfReinforcement = datetime.strptime(timeOfReinforcementAsAString, '%Y-%m-%d %H:%M:%S')

        totalSecondsElapsedSinceReinforcement = int((timeOfReinforcement - self.experimentStartTime).total_seconds())

        self.xCoordinates.append( totalSecondsElapsedSinceReinforcement )

        self.yCoordinates.append( BIndex + 0.01 * self.robotColorIndex )

    def Handle_Robot(self,robot):

        self.xCoordinates = []

        self.yCoordinates = []

        self.robotID = self.db.From_Robot_Record_Get_ID(robot)

        self.robotColorIndex = self.db.From_Robot_Record_Get_Color_Index(robot)

        self.Add_Robot_Creation_Date(robot)

        reinforcements = self.db.Get_Reinforcements_For_Robot(self.robotID)

        for self.reinforcement in reinforcements:

            self.Handle_Reinforcement()

        self.Draw_Robots_BIndices()

    def Prep_Drawing(self):

        plt.rcParams.update({'font.size': 22})

        self.fig, self.ax = plt.subplots(1)
        self.fig.patch.set_facecolor('green')
        self.fig.patch.set_alpha(0.0)

    def Seconds_Elapsed_So_Far(self):

        totalSecondsElapsed = int((datetime.now() - self.experimentStartTime).total_seconds())

        return totalSecondsElapsed
