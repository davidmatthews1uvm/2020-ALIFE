import os

import time

import constants as c

import constantsPassiveGame as cpg

from passiveGame.option import OPTION

class OPTIONS:

    def __init__(self,database):

        self.database = database

        self.color = 'r'

        self.command = '!jump'

        self.options = {}

        for option in range(0,cpg.numOptions):

            self.options[option] = OPTION(option)

        self.timeOfLastUpdate = time.time()

        self.Set_Locked_Conditions()

    def Draw_To(self,screen,highestScore,maxPts,ptsPerSec):

        for option in self.options:

            if self.Is_Not_Affordable(option,highestScore):

                self.options[option].Draw_Question_Marks(screen) 

                # self.options[option].Do_Not_Draw()

            elif self.options[option].Is_Unlock_Env_Option() and self.noLockedEnvs:

                self.options[option].Do_Not_Draw()

            elif self.options[option].Is_Affordable(highestScore):

                self.options[option].Draw_White_To(screen)
 
            else: # It's almost affordable

                self.options[option].Draw_Gray_To(screen,maxPts,ptsPerSec)

    def Update(self):

        secondsSinceLastUpdate = time.time() - self.timeOfLastUpdate

        if secondsSinceLastUpdate > cpg.timeBetweenOptionsUpdates:

            self.Try_To_Update()

            self.timeOfLastUpdate = time.time()

# ------------- Private methods ---------------------

    def Is_Cheapest_Option(self,option):

        return option == ( cpg.numOptions - 1 )
        
    def Is_Not_Affordable(self,option,highestScore):

        if highestScore == 0:

            return self.Is_Cheapest_Option(option) == False

        if self.options[option].Is_Affordable(highestScore):

            return False

        if self.Is_Cheapest_Option(option):

            return False

        thisOptionsCost = self.options[option].Get_Cost()

        nextCheapestOption = option + 1

        nextChepeastOptionsCost = self.options[nextCheapestOption].Get_Cost()

        if thisOptionsCost > nextChepeastOptionsCost:

            return self.options[nextCheapestOption].Is_Too_Expensive(highestScore)

        else: # The costs are equal

            return self.options[option+2].Is_Too_Expensive(highestScore)

    def No_Locked_Bots(self):

        bots = self.database.Get_Locked_Robots()

        return bots == []

    def No_Locked_Envs(self):

        envs = self.database.Get_Locked_Environments()

        return envs == []

    def Replace_Color_In_Options(self,aggressorColor,defenderColor):

        newDefenderColorName = c.colorNameDict[defenderColor]


        self.options[cpg.stealRequest].Replace_Last_Word_In_What_Can_I_Do_With( newDefenderColorName )

        self.options[cpg.stealRequest].Set_What_Do_I_Type_To( 's' + defenderColor )


        self.options[cpg.buyRequest].Replace_Last_Word_In_What_Can_I_Do_With( newDefenderColorName )

        self.options[cpg.buyRequest].Set_What_Do_I_Type_To( 'b' + defenderColor )


        newAggressorColorName = c.colorNameDict[aggressorColor]

        self.options[cpg.aggressorReinforcementRequest].Replace_Second_Word_In_What_Can_I_Do_With( newAggressorColorName ) 

        self.options[cpg.aggressorReinforcementRequest].Set_What_Do_I_Type_To( aggressorColor )


        self.options[cpg.defenderReinforcementRequest].Replace_Second_Word_In_What_Can_I_Do_With( newDefenderColorName )

        self.options[cpg.defenderReinforcementRequest].Set_What_Do_I_Type_To( defenderColor )

    def Replace_Command_In_Options(self,command):

        self.options[cpg.aggressorReinforcementRequest].Replace_Command_In_What_Can_I_Do_With( command )

    def Replace_Number_In_Unlock_Env_Option(self):

        if self.No_Locked_Envs():

            return

        lockedEnv = self.database.Get_Lowest_Numbered_Locked_Environment()

        environmentID = self.database.From_Environment_Record_Get_ID(lockedEnv)

        lockedEnvironmentName = str(environmentID) 

        self.options[cpg.unlockEnvRequest].Replace_Last_Word_In_What_Can_I_Do_With( lockedEnvironmentName )

        self.options[cpg.unlockEnvRequest].Set_What_Do_I_Type_To( 'u' + lockedEnvironmentName ) 

    def Set_Locked_Conditions(self):

        self.noLockedBots = self.No_Locked_Bots()

        self.noLockedEnvs = self.No_Locked_Envs()

    def Try_To_Update(self):

        lastTwoEvaluations = self.database.Get_Last_Two_Evaluations()

        if not lastTwoEvaluations:

            return

        if len(lastTwoEvaluations) < 2:

            return

        aggressorEvaluation = lastTwoEvaluations[0]

        defenderEvaluation  = lastTwoEvaluations[1]  

        self.Set_Locked_Conditions()

        self.Replace_Number_In_Unlock_Env_Option()

        aggressorColor   = self.database.From_Evaluation_Record_Get_RobotColor(aggressorEvaluation)

        defenderColor    = self.database.From_Evaluation_Record_Get_RobotColor(defenderEvaluation)

        self.Replace_Color_In_Options(aggressorColor,defenderColor)

        command = self.database.From_Evaluation_Record_Get_Command(defenderEvaluation)

        # self.Replace_Command_In_Options(command)
