import random

import constants as c

from reinforcement    import REINFORCEMENT
from win              import WIN
from loss             import LOSS

class REINFORCEMENTS:

    def __init__(self):

        self.reinforcements = {}

    def Are_Empty(self):

        return self.reinforcements == {}

    def Draw_To(self,screen):

        for r in self.reinforcements:

            self.reinforcements[r].Draw_To(screen)

            self.reinforcements[r].Draw_Robots_Wins_Or_Losses()

    def Load_New_Ones(self,database,robots):

        reinforcementPair = database.Get_Newest_Pair_Of_Undigested_Reinforcements()

        if not reinforcementPair:

            return

        if len(reinforcementPair)<2:

            return

        firstReinforcement = reinforcementPair[0]
        secondReinforcement = reinforcementPair[1]

        yesOrNo = database.From_Reinforcement_Record_Get_Signal(firstReinforcement)

        if yesOrNo == 'y':

           win  = firstReinforcement
           loss = secondReinforcement
        else:
           win  = secondReinforcement
           loss = firstReinforcement

        winID                       = database.From_Reinforcement_Record_Get_ID(win)
        lossID                      = database.From_Reinforcement_Record_Get_ID(loss)

        winningRobotID              = database.From_Reinforcement_Record_Get_Robot_ID(win)
        losingRobotID               = database.From_Reinforcement_Record_Get_Robot_ID(loss)

        winningRobot                = database.Get_Robot_By_ID(winningRobotID)
        losingRobot                 = database.Get_Robot_By_ID(losingRobotID)

        winningColorIndex           = database.From_Robot_Record_Get_Color_Index(winningRobot)
        losingColorIndex            = database.From_Robot_Record_Get_Color_Index(losingRobot)

        winColor                    = c.colors[winningColorIndex]
        lossColor                   = c.colors[losingColorIndex]

        numUndigestedReinforcements = database.Get_Num_Undigested_Reinforcements()

        userID                      = database.From_Reinforcement_Record_Get_User_ID(win)

        user                        = database.Get_User_By_ID(userID)

        username                    = database.From_User_Record_Get_Name(user)

        self.reinforcements['win']  = WIN(winID,robots,winColor,numUndigestedReinforcements,username)

        self.reinforcements['loss'] = LOSS(lossID,robots,lossColor,numUndigestedReinforcements,username)

    def Update(self,database):

        for r in list(self.reinforcements.keys()):

            self.reinforcements[r].Update()

            if self.reinforcements[r].Done():

                self.reinforcements[r].Digest(database)

                self.reinforcements[r].Add_To_Robot()

                del self.reinforcements[r]
