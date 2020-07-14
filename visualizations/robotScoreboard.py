import matplotlib.pyplot as plt
import numpy as np
import random

import sys


from database.database import DATABASE

import constants as c

from visualizations.matrix import MATRIX

class ROBOT_SCORE_BOARD:

    def __init__(self):

        self.db = DATABASE()

        self.robots = self.db.Get_Living_Robots()

        self.numColumns = len(self.robots)

        self.commands = self.db.Get_Unique_Commands()

        random.shuffle(self.commands)

        while len(self.commands) > 10:

            del self.commands[-1]

        self.numRows = len(self.commands)

        self.cellWidth = 10

        self.matrix = MATRIX( numRows = self.numRows , numColumns = self.numColumns , cellWidth = self.cellWidth )

        self.Set_Cell_Colors()

        self.Set_Cell_Contents()

    def Draw(self,primaryBotIndex):

        plt.rcParams.update({'font.size': 14})
        plt.rcParams.update({'font.family': 'monospace'})

        self.fig, self.ax = plt.subplots(1)
        self.fig.patch.set_facecolor('green')
        self.fig.patch.set_alpha(0.0)

        self.matrix.Draw(self.ax,primaryBotIndex)

        self.Draw_Commands()

        self.Underline_Rows()

        self.Clean_Up(self.ax,primaryBotIndex)

    def Print(self):

        self.matrix.Print()

    def Save(self,primaryBotIndex):

        self.Draw(primaryBotIndex)

        plt.savefig('test.png', transparent=True)
        self.fig.clf()

        del self.fig
        del self.ax

        plt.close()


    def Sufficient_Conditions_For_Drawing(self):
        return True

# -------------- Private methods -------------------------

    def Clean_Up(self,ax,primaryBotIndex):

        plt.axis([ self.matrix.Left() , self.matrix.Right() , self.matrix.Bottom() , self.matrix.Top() ])

        ax.set_xticks([])

        ax.set_yticks([])

        ax.set_title('Yes votes for the ' + c.colorNamesNoParens[primaryBotIndex] + ' robot.')

    def Draw_Commands(self):

        for i in range(0,self.numRows):

            command = self.commands[ i ] 

            commandString = '!' + self.db.From_UniqueCommand_Record_Get_String(command) 

            self.matrix.On_Row_Draw_Text(i , commandString )

    def Set_Cell_Colors(self):

        for i in range(0,self.numRows):

            command = self.commands[ i ]

            for j in range(0,self.numColumns):

                robotColor = c.colorRGBs[ j ]

                self.matrix.Set_Cell_Color( i , j , robotColor )

    def Set_Cell_Contents(self):

        for i in range(0,self.numRows):

            command = self.commands[ i ]

            commandString = self.db.From_UniqueCommand_Record_Get_String(command)

            for j in range(0,self.numColumns):

                robot = self.robots[ j ]

                robotID = self.db.From_Robot_Record_Get_ID(robot)

                numYesVotes = self.db.Get_Yes_Votes_For_Robot_Under_Command(robotID,commandString)

                self.matrix.Set_Cell_Contents( i , j , str(numYesVotes) )

    def Underline_Rows(self):

        self.matrix.Underline_Rows()

# -------------- Main function ---------------------------

# robotScoreboard = ROBOT_SCORE_BOARD()

# robotScoreboard.Print()

# robotScoreboard.Draw(primaryBotIndex = 9)

