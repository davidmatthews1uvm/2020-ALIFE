import copy
import gc
import os
import pickle
import random

import numpy as np

import constants as c
from TPR_3.robot import ROBOT
from database.database import DATABASE
from environments.env_ball import ENV_BALL
from environments.env_cube_green_front import ENV_CUBE_GREEN_FRONT
from environments.env_cube_green_front_immobile import ENV_CUBE_GREEN_FRONT_IMMOBILE
from environments.env_cube_green_left import ENV_CUBE_GREEN_LEFT
from environments.env_cube_greenandred_front import ENV_CUBE_GREENANDRED_FRONT
from environments.env_monkeybars import ENV_MONKEYBARS
from environments.env_ramp import ENV_RAMP
from environments.env_seesaw import ENV_SEESAW
from environments.env_slingshot import ENV_SLINGSHOT
from environments.env_stairs import ENV_STAIRS
from environments.environment0 import ENVIRONMENT0
from environments.environment1 import ENVIRONMENT1
from pyrosim.pyrosim import pyrosim
from visualizations.cumulativeYesVotes import CUMULATIVE_YES_VOTES
from visualizations.paretoFront import PARETO_FRONT
from visualizations.phylotree import PHYLOTREE


class EVOLVER:

    def __init__(self):
        self.Print_Preamble()
        self.database = DATABASE()
        self.nextAvailableRobotID = 0
        self.Initialize()

    def Advance_To_Next_Visualization_Type(self):
        self.whichVisualizationToDraw = self.whichVisualizationToDraw + 1

        if (self.whichVisualizationToDraw == c.VISUALIZATION_TYPES):
            self.whichVisualizationToDraw = 0

    def Choose_Aggressor_And_Defender(self):
        if (self.database.No_Negative_Reinforcements()):
            self.Choose_Random_Aggressor_And_Defender()
            return

        candidateDefenderID = self.database.Get_Most_Recently_Negatively_Reinforced_Bot()
        candidateDefenderPosition = self.Get_Position_From_ID(candidateDefenderID)

        if (self.database.Bot_Is_Dead(candidateDefenderID)):
            self.Choose_Random_Aggressor_And_Defender()
            return

        candidateAggressorPosition = self.Find_Valid_Aggressor(candidateDefenderID)

        if (candidateAggressorPosition == -1):
            self.Choose_Random_Aggressor_And_Defender()
            return

        self.defenderPosition = candidateDefenderPosition
        self.defenderID = candidateDefenderID
        self.aggressorPosition = candidateAggressorPosition
        self.aggressorID = self.Get_ID_At_Position(self.aggressorPosition)

    def Choose_Random_Defender(self):
        self.defenderPosition = random.randint(0, c.popSize - 1)

        while ((self.defenderPosition == self.aggressorPosition) or self.Robot_Was_Just_Shown(self.defenderPosition)):
            self.defenderPosition = random.randint(0, c.popSize - 1)

        self.defenderID = self.robots[self.defenderPosition].ID

    def Choose_Random_Aggressor(self):
        self.aggressorPosition = random.randint(0, c.popSize - 1)

        while (self.Robot_Was_Just_Shown(self.aggressorPosition)):
            self.aggressorPosition = random.randint(0, c.popSize - 1)

        self.aggressorID = self.robots[self.aggressorPosition].ID

    def Choose_Random_Aggressor_And_Defender(self):
        self.Choose_Random_Aggressor()
        self.Choose_Random_Defender()

    def Command_Available(self):
        return self.database.Command_Available()

    def Draw_Cumulative_Yes_Votes(self):
        cyv = CUMULATIVE_YES_VOTES()

        if cyv.Sufficient_Conditions_For_Drawing():
            cyv.Collect_Data()
            cyv.Save()

    def Draw_Empty_Phylo_Tree(self):
        phyloTree = PHYLOTREE(self.database)
        phyloTree.Draw_Empty()

    def Draw_Pareto_Front(self, primaryBotPosition):
        paretoFront = PARETO_FRONT(self.database)
        paretoFront.Draw(self.robots, primaryBotPosition)

    def Draw_Phylo_Tree(self, primaryBotPosition, secondaryBotPosition):
        phyloTree = PHYLOTREE()
        primaryBotID = -1

        if (primaryBotPosition > -1):
            primaryBotID = self.robots[primaryBotPosition].ID

        secondaryBotID = -1

        if (secondaryBotPosition > -1):
            secondaryBotID = self.robots[secondaryBotPosition].ID

        phyloTree.Draw(self.robots, primaryBotID, secondaryBotID)

    def Draw_Visualization(self, primaryBotPosition, secondaryBotPosition):

        while (self.Sufficient_Conditions_For_Current_Visualization_Type() == False):
            self.Advance_To_Next_Visualization_Type()

        if (self.whichVisualizationToDraw == c.DRAW_PHYLO_TREE):
            self.Draw_Phylo_Tree(primaryBotPosition, secondaryBotPosition)
        elif (self.whichVisualizationToDraw == c.DRAW_PARETO_FRONT):
            self.Draw_Pareto_Front(primaryBotPosition)
        else:
            self.Draw_Cumulative_Yes_Votes()

        self.Advance_To_Next_Visualization_Type()
        gc.collect()

    def Find_Valid_Aggressor(self, defenderID):
        defenderPosition = self.Get_Position_From_ID(defenderID)
        candidateAggressors = np.random.permutation(c.popSize)
        validAggressorPosition = -1

        for aggressorPosition in candidateAggressors:
            aggressorID = self.Get_ID_At_Position(aggressorPosition)
            aggressorDiffersFromDefender = aggressorID != defenderID
            aggressorCanKillDefender = self.database.Aggressor_Can_Kill_Defender(aggressorID, defenderID)
            aggressorNotJustEvaluated = (self.Robot_Was_Just_Evaluated(aggressorPosition) == False)

            if (aggressorDiffersFromDefender and aggressorCanKillDefender and aggressorNotJustEvaluated):
                validAggressorPosition = aggressorPosition

        return validAggressorPosition

    def Get_ID_At_Position(self, position):
        return self.robots[position].ID

    def Get_Position_From_ID(self, ID):
        position = -1

        for p in range(0, c.popSize):
            if (self.robots[p].ID == ID):
                position = p

        return position

    def Handle_User_Issued_Commands(self):
        if (self.Command_Available()):
            self.command = self.database.Get_Command_From_Queue()

            if (self.database.Command_Is_New(self.command)):
                self.database.Add_Unique_Command(self.command)

            self.database.Delete_Command_From_Queue()
            self.Signal_Command_Change_To_Users()
        else:
            if (self.command != c.defaultCommand):
                self.command = c.defaultCommand
                self.Signal_Command_Change_To_Users()

    def Initialize(self):
        self.robots = {}
        self.originalBots = {}

        for p in range(0, c.popSize):
            self.Spawn_Bot(p)

        self.previousAggressorPosition = -1
        self.previousDefenderPosition = -1
        self.command = c.defaultCommand

        if (self.database.Command_Is_New(self.command)):
            self.database.Add_Unique_Command(self.command)

        self.whichVisualizationToDraw = c.DRAW_PHYLO_TREE

    def Load_Robot(self, position):
        filename = "../school/students/student" + str(position) + ".p"
        self.robots[position] = pickle.load(open(filename, 'rb'))
        self.robots[position].Set_ID(self.nextAvailableRobotID)
        self.Delete_Robot(position)

    def Delete_Robot(self, position):
        filename = "../school/students/student" + str(position) + ".p"
        os.remove(filename)

    def Perform_Housekeeping(self):
        self.database.Push_To_Dropbox()
        self.database.Delete_Old_And_Non_Reinforced_Evaluations()

    def Perform_Ten_Evaluations(self):
        for i in range(0, 10):
            self.Simulate_Competition()

        self.Simulate_All_Bots()

    def Print_Info(self, color):
        print('It was just told to !' + self.command + '.')
        print('')

        print('Type             ' + color + 'y   if it is.')
        print('')

        print('Type             ' + color + 'n   otherwise.')
        print('')

        print('Type             ?    to learn more.')

    def Print_Preamble(self):
        for i in range(0, 100):
            print('')

    def Reinforcements_Received(self):
        return self.database.Total_Positive_Reinforcements() > 1

    def Robot_Available(self, position):
        filename = "../school/students/student" + str(position) + ".p"

        return os.path.isfile(filename)

    def Robot_Was_Just_Evaluated(self, position):
        return (position == self.previousAggressorPosition)

    def Robot_Was_Just_Shown(self, position):
        return (position == self.previousAggressorPosition) or (position == self.previousDefenderPosition)

    def Run_Sim(self, s, primaryBotPosition, secondaryBotPosition):
        s.assign_collision('robot', 'env')
        s.assign_collision('env', 'env')
        s.start()

        # self.Draw_Visualization(primaryBotPosition, secondaryBotPosition)

    def Send_Bot_And_Environment(self, s, b, physicsOffset, drawOffset, fadeStrategy):
        environmentIndex = random.randint(0, c.NUM_ENVIRONMENTS_AVAILABLE - 1)

        if (environmentIndex == 0):
            environment = ENVIRONMENT0(s)
        if (environmentIndex == 1):
            environment = ENVIRONMENT1(s)
        if (environmentIndex == 2):
            environment = ENV_BALL(s)
        if (environmentIndex == 3):
            environment = ENV_MONKEYBARS(s)
        if (environmentIndex == 4):
            environment = ENV_RAMP(s)
        if (environmentIndex == 5):
            environment = ENV_SEESAW(s)
        if (environmentIndex == 6):
            environment = ENV_SLINGSHOT(s)
        if (environmentIndex == 7):
            environment = ENV_STAIRS(s)
        if (environmentIndex == 8):
            environment = ENV_CUBE_GREENANDRED_FRONT(s)
        if (environmentIndex == 9):
            environment = ENV_CUBE_GREEN_FRONT(s)
        if (environmentIndex == 10):
            environment = ENV_CUBE_GREEN_FRONT_IMMOBILE(s)
        if (environmentIndex == 11):
            environment = ENV_CUBE_GREEN_LEFT(s)

        environment.Send_To_Simulator(physicsOffset, drawOffset, fadeStrategy)
        bot = copy.deepcopy(b)
        bot.Reset()
        summedPhysicsOffset = tuple(map(sum, zip(environment.Get_Robot_Offset(), physicsOffset)))

        del environment

        commandEncoding = self.database.Get_Command_Encoding(self.command)
        bot.Send_To_Simulator(s, summedPhysicsOffset, drawOffset, fadeStrategy, commandEncoding)

    def Signal_Command_Change_To_Users(self):
        self.Print_Preamble()
        print('The next robot is about to hear the command !' + self.command + '.')
        self.Simulate_Empty_World()

    def Simulate_All_Bots(self):
        self.Simulate_All_Original_Bots()
        self.Simulate_All_Current_Bots()

    def Simulate_All_Current_Bots(self):
        s = pyrosim.Simulator(debug=False, play_paused=False, eval_time=c.evaluationTime)

        for r in range(0, c.popSize):
            self.Send_Bot_And_Environment(s, self.robots[r], c.swarmPositionOffsets[r], c.swarmDrawOffsets[r], c.noFade)

        self.Print_Preamble()

        print('...and these are the current bots.')
        print('')

        print('Are they doing a better job at obeying the command !' + self.command + '?')
        print('')

        print('')
        print('')

        print('')

        s.start()

        self.Draw_Visualization(-1, -1)
        self.Perform_Housekeeping()

        s.wait_to_finish()

    def Simulate_All_Original_Bots(self):
        s = pyrosim.Simulator(debug=False, play_paused=False, eval_time=c.evaluationTime)

        for r in range(0, c.popSize):
            self.Send_Bot_And_Environment(s, self.originalBots[r], c.swarmPositionOffsets[r], c.swarmDrawOffsets[r],
                                          c.noFade)

        self.Print_Preamble()

        print('These were the original bots...')
        print('')

        print('')
        print('')

        print('')
        print('')

        print('')

        s.start()

        self.Draw_Visualization(-1, -1)

        s.wait_to_finish()

    def Simulate_Birth_From_Aggressor(self):
        self.Spawn_From_Aggressor()
        s = pyrosim.Simulator(eval_time=c.evaluationTime)
        self.Store_Evaluation(self.defenderPosition)
        self.Send_Bot_And_Environment(s, self.robots[self.defenderPosition], [0, 0, 0], [0, 0, 0], c.fadeIn)
        self.Send_Bot_And_Environment(s, self.robots[self.aggressorPosition], [-100, +100, 0], [100 - 1, -100 + 1, 0],
                                      c.noFade)
        self.Print_Preamble()

        colorOfNewBot = c.colorNames[self.defenderPosition]

        print('This is the new ' + colorOfNewBot + ' bot, just spawned by the bot above.')
        print('')

        color = c.colors[self.defenderPosition]

        self.Print_Info(color)
        self.Run_Sim(s, self.defenderPosition, self.aggressorPosition)

        s.wait_to_finish()

    def Simulate_Birth_De_Novo(self):
        self.Spawn_De_Novo(self.defenderPosition)
        s = pyrosim.Simulator(eval_time=c.evaluationTime)
        self.Store_Evaluation(self.defenderPosition)
        self.Send_Bot_And_Environment(s, self.robots[self.defenderPosition], [0, 0, 0], [0, 0, 0], c.fadeIn)
        self.Print_Preamble()

        colorOfNewBot = c.colorNames[self.defenderPosition]

        print('This is the new ' + colorOfNewBot + ' bot, just spawned from scratch.')
        print('')

        color = c.colors[self.defenderPosition]

        self.Print_Info(color)
        self.Run_Sim(s, self.defenderPosition, -1)

        s.wait_to_finish()

    def Simulate_Competition(self):
        self.Handle_User_Issued_Commands()
        self.Choose_Aggressor_And_Defender()
        aggressorKilledDefender = self.database.Aggressor_Can_Kill_Defender(self.aggressorID, self.defenderID)

        if (aggressorKilledDefender):
            self.Simulate_Death()
            if (random.randint(0, 1) == 0):
                self.Simulate_Birth_From_Aggressor()
            else:
                self.Simulate_Birth_De_Novo()
        else:
            self.Simulate_Survival()

        self.previousAggressorPosition = self.aggressorPosition
        self.previousDefenderPosition = self.defenderPosition

    def Simulate_Death(self):
        s = pyrosim.Simulator(eval_time=c.evaluationTime)
        self.Store_Evaluation(self.aggressorPosition)
        self.Send_Bot_And_Environment(s, self.robots[self.aggressorPosition], [0, 0, 0], [0, 0, 0], c.noFade)
        self.Send_Bot_And_Environment(s, self.robots[self.defenderPosition], [-100, +100, 0], [100 - 1, -100 + 1, 0],
                                      c.fadeOut)
        self.Print_Preamble()
        botColorName = c.colorNames[self.aggressorPosition]

        print('This is the     ' + botColorName + ' bot, which just killed the bot above.')
        print('')

        color = c.colors[self.aggressorPosition]

        self.Print_Info(color)
        self.Run_Sim(s, self.aggressorPosition, self.defenderPosition)

        s.wait_to_finish()

        self.database.Kill_Bot(self.defenderID)

    def Simulate_Empty_World(self):
        s = pyrosim.Simulator(debug=False, play_paused=False, eval_time=c.evaluationTime)
        s.start()
        s.wait_to_finish()

    def Simulate_Survival(self):

        s = pyrosim.Simulator(debug=False, play_paused=False, eval_time=c.evaluationTime)
        self.Store_Evaluation(self.aggressorPosition)
        self.Send_Bot_And_Environment(s, self.robots[self.aggressorPosition], [0, 0, 0], [0, 0, 0], c.noFade)
        self.Print_Preamble()

        botColorName = c.colorNames[self.aggressorPosition]

        print('This is the     ' + botColorName + ' bot.')
        print('')

        color = c.colors[self.aggressorPosition]
        self.Print_Info(color)
        self.Run_Sim(s, self.aggressorPosition, -1)
        s.wait_to_finish()

    def Spawn_Bot(self, position):
        self.Spawn_De_Novo(position)
        self.originalBots[position] = copy.deepcopy(self.robots[position])

    def Spawn_De_Novo(self, position):
        if (self.Robot_Available(position)):
            self.Load_Robot(position)
        else:
            self.robots[position] = ROBOT(ID=self.nextAvailableRobotID,
                                          colorIndex=position,
                                          parentID=-1,
                                          clr=c.colorRGBs[position])

        self.database.Add_Robot(self.robots[position])
        self.database.Unlock_Bot(self.nextAvailableRobotID)
        self.nextAvailableRobotID = self.nextAvailableRobotID + 1



    def Spawn_From_Aggressor(self):
        newBotPosition = self.defenderPosition

        self.robots[newBotPosition] = copy.deepcopy(self.robots[self.aggressorPosition])
        self.robots[newBotPosition].Mutate()
        self.robots[newBotPosition].ID = self.nextAvailableRobotID
        self.robots[newBotPosition].colorIndex = newBotPosition
        self.robots[newBotPosition].parentID = self.robots[self.aggressorPosition].ID
        self.robots[newBotPosition].Set_Color(c.colorRGBs[newBotPosition])
        self.nextAvailableRobotID = self.nextAvailableRobotID + 1
        self.database.Add_Robot(  self.robots[newBotPosition])
        self.database.Unlock_Bot( self.robots[newBotPosition].Get_ID() )

    def Store_Evaluation(self, position):
        self.database.Add_Evaluation(self.robots[position].ID, c.colors[position], self.command)

    def Sufficient_Conditions_For_Current_Visualization_Type(self):

        if (self.whichVisualizationToDraw == c.DRAW_PHYLO_TREE):
            pt = PHYLOTREE()
            return pt.Sufficient_Conditions_For_Drawing()
        elif (self.whichVisualizationToDraw == c.DRAW_PARETO_FRONT):
            pf = PARETO_FRONT(self.database)
            return pf.Sufficient_Conditions_For_Drawing()
        else:
            cyv = CUMULATIVE_YES_VOTES()
            return cyv.Sufficient_Conditions_For_Drawing()
