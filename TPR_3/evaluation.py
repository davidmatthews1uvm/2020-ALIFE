import sys

from pyrosim.pyrosim import pyrosim


import constants as c

from environments.environment import ENVIRONMENT

class EVALUATION:

    def __init__(self,database,simulator,environment,robotPosition,robot,command,speed,simulationType,oldRobotColor=0):

        self.database = database

        self.simulator = simulator

        self.environment = environment

        self.robotPosition = robotPosition

        self.robot = robot

        self.command = command

        self.speed = speed

        self.simulationType = simulationType

        self.oldRobotColor = oldRobotColor

    def Set_Drawing_Conditions(self,index):

        self.positionOffset = c.swarmPositionOffsets[index] 

        self.drawOffset = c.swarmDrawOffsets[index] 

        if ( (self.simulationType == c.SIMULATE_DEATH) and (index==0) ):

            self.fadeStrategy = c.fadeOut

        elif ( (self.simulationType == c.SIMULATE_BIRTH_DE_NOVO) and (index==0) ):

            self.fadeStrategy = c.fadeIn

        elif ( (self.simulationType == c.SIMULATE_BIRTH_FROM_AGGRESSOR) and (index==0) ):

            self.fadeStrategy = c.fadeIn

        #SIMULATE_DEATH_FROM_OLD_AGE ([0] child fades in, [1] dying parent fades out)
        elif ( (self.simulationType == c.SIMULATE_DEATH_FROM_OLD_AGE) and (index==0) ):

            self.fadeStrategy = c.fadeOut

        else:
            self.fadeStrategy = c.noFade
      
    def Start(self):

        self.environment.Send_To_Simulator( self.positionOffset , self.drawOffset , self.fadeStrategy )

        summedPositionOffset = tuple(map(sum, zip(self.environment.Get_Robot_Offset(), self.positionOffset)))

        self.robot.Send_To_Simulator( self.simulator , summedPositionOffset, self.drawOffset, self.fadeStrategy, currentCommandEncoding = self.command.Get_Encoding() )

    def Store_In_Database(self):

        self.database.Add_Evaluation(self.robot.ID, c.colors[self.robotPosition], self.command.Get_String(), self.speed, self.environment.Get_Index(), self.simulationType)
