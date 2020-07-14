import random
import pickle

from pyrosim.pyrosim import pyrosim

import constants as c

from TPR_3.environment import ENVIRONMENT
from TPR_3.command import COMMAND
from TPR_3.visualization import VISUALIZATION
from TPR_3.messageToCrowd import MESSAGE_TO_CROWD
from TPR_3.evaluation import EVALUATION
from TPR_3.speech import SPEECH

class SIMULATION:

    def __init__(self,simulationType,database,positionsOfRobotsBeingSimulated,robots, play_blind=False, silent_mode=True, oldRobotID=-1):

        self.simulationType = simulationType

        self.database = database

        self.robots = robots

        self.oldRobotID = oldRobotID

        self.positionsOfRobotsBeingSimulated = positionsOfRobotsBeingSimulated

        self.Determine_Speed()

        self.simulator = pyrosim.Simulator(play_blind=play_blind, play_paused=False, eval_time=c.evaluationTime * c.ACCURACY, dt = 0.05 / c.ACCURACY, silent_mode=silent_mode, window_size=(375, 250), speed=self.speed * c.ACCURACY , xyz = [0.8317*2,-0.9817*2,0.8000*2], hpr = [121,-27.5*0.75,0.0])

        self.environment = ENVIRONMENT( self.database , self.simulator )

        self.command = COMMAND( self.database, distribution="ranked" )

        self.visualization = VISUALIZATION( self.database , self.positionsOfRobotsBeingSimulated, self.robots, oldRobotID=self.oldRobotID )

        self.messageToCrowd = MESSAGE_TO_CROWD( self.simulationType , self.robots, self.positionsOfRobotsBeingSimulated , self.command.Get_String(), self.speed, self.database, self.environment.Get_Index() )

        if self.simulationType == c.SIMULATE_SURVIVAL:
 
            self.speech = SPEECH( self.command , self.positionsOfRobotsBeingSimulated )
        else:
            self.speech = None

        self.Initialize_Evaluations()

    def End(self):

        self.database.Delete_Non_Reinforced_Evaluations()

        self.simulator.wait_to_finish()

    def Start(self):

        self.messageToCrowd.Print()

        for evaluation in self.evaluations:

            self.evaluations[evaluation].Start()

        if ( (self.simulationType == c.SIMULATE_ALL) or (self.simulationType == c.SIMULATE_ALL_ORIGINAL_BOTS) ):

            self.visualization.Save_Empty_Image()

        else:

            self.visualization.Save()

        self.simulator.assign_collision('robot', 'env')

        self.simulator.assign_collision('env', 'env')

        self.simulator.start()

        for evaluation in self.evaluations:

            self.evaluations[evaluation].Store_In_Database()

        if self.speech:

            self.speech.start(self.speed)

# ----------------- Private methods ------------------------------------

    def Above_Min_Speed(self):

        return self.speed > c.MINIMUM_SPEED

    def Below_Max_Speed(self):

        return self.speed < c.MAXIMUM_SPEED

    def Determine_Speed(self):

        if self.No_Evaluations_Yet():

            self.speed = c.DEFAULT_SPEED
 
        else:
            self.Determine_Speed_Based_On_Previous_Speed()

    def Determine_Speed_Based_On_Previous_Speed(self):

        lastEvaluation = self.database.Get_Current_Evaluation() # New evaluation hasn't started yet.

        self.speed = self.database.From_Evaluation_Record_Get_Speed(lastEvaluation)
      
        speedChangeRequest = self.database.Get_Speed_Change_Request()

        if speedChangeRequest:

            self.Honor_Request_To_Change_Speed(speedChangeRequest)

    def Honor_Request_To_Change_Speed(self,speedChangeRequest):

        fasterOrSlower = self.database.From_Speed_Change_Request_Record_Get_Faster_Or_Slower(speedChangeRequest)

        if fasterOrSlower == '+' and self.Below_Max_Speed():

            self.speed = self.speed + 1

        elif fasterOrSlower == '-' and self.Above_Min_Speed():

            self.speed = self.speed - 1

        speedChangeID = self.database.From_Speed_Change_Request_Record_Get_ID(speedChangeRequest)

        self.database.Set_Speed_Change_Request_Honored(speedChangeID)

    def Initialize_Evaluations(self):

        self.evaluations = {}

        evaluationIndex = 0

            ################################################################################
        for robotPosition in self.positionsOfRobotsBeingSimulated:
            
            robot = self.robots[robotPosition]

            if self.simulationType == c.SIMULATE_BEST:
                
                colorIndex, BIndex = self.database.Get_Color_Index_And_Highest_B_Index_Among_Living_Robots()

                indicesOfTwoRandomlyChosenCommands = random.sample(range(0,BIndex),2)

                n = indicesOfTwoRandomlyChosenCommands[evaluationIndex] 

                robotID = self.robots[robotPosition].ID

                commandString = self.database.Get_Nth_Command_Obeyed_By_Robot(n,robotID)

                self.messageToCrowd.Add_Command_Obeyed_By_Best_Bot(commandString)

                nthCommand = COMMAND(self.database, distribution="ranked")
                nthCommand.Set_String(commandString)

                self.evaluations[evaluationIndex] = EVALUATION( self.database, self.simulator, self.environment, robotPosition, robot , nthCommand, self.speed,self.simulationType)
            
            elif self.simulationType == c.SIMULATE_DEATH_FROM_OLD_AGE:
                    
                filenameOfOldRobot = '../data/robot' + str(self.oldRobotID) + '.p'
                
                robot = pickle.load( open( filenameOfOldRobot , 'rb' ) )

                self.evaluations[evaluationIndex] = EVALUATION( self.database, self.simulator, self.environment, robotPosition, robot , self.command, self.speed,self.simulationType, oldRobotColor=self.positionsOfRobotsBeingSimulated[0])
                
            else:
                
                self.evaluations[evaluationIndex] = EVALUATION( self.database, self.simulator, self.environment, robotPosition, robot , self.command, self.speed,self.simulationType)

            self.evaluations[evaluationIndex].Set_Drawing_Conditions(evaluationIndex)

            evaluationIndex = evaluationIndex + 1

    def No_Evaluations_Yet(self):

        lastEvaluation = self.database.Get_Current_Evaluation() # New evaluation hasn't started yet.

        return not lastEvaluation
