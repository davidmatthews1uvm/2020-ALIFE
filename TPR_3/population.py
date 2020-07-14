import copy
import numpy as np
import os
import pickle
import random
import sys
import constants as c
import datetime

from TPR_3.simulation import SIMULATION

from TPR_3.robot import ROBOT

class POPULATION():

    def __init__(self,database,testing=False):
        self.testing = testing
        self.database = database

        self.robots = {}

        self.Get_Living_Robots()

        self.originalRobots = {}

        self.Get_Original_Robots()

        self.defenderPosition = None
        self.aggressorPosition = None

        self.Retrieve_Robot_Locked_Statuses()

    def Perform_One_Simulation(self):

        self.Determine_Simulation_Type()

        self.simulation = SIMULATION( self.simulationType , self.database , self.positionsOfRobotsBeingSimulated , self.robots, play_blind=self.testing, oldRobotID = self.oldRobotID)

        self.simulation.Start()

        if self.simulationType == c.SIMULATE_DEATH:

            defenderID = self.robots[self.defenderPosition].ID

            self.database.Kill_Bot(defenderID)

            del self.robots[self.defenderPosition]

        elif self.simulationType == c.SIMULATE_DEATH_FROM_OLD_AGE:
            
            self.database.Kill_Bot(self.oldRobotID)

            del self.robots[self.indexOfOldRobot]

        self.simulation.End()

# ------------ Private methods ------------------

    def Aggressor_Kills_Defender(self):

        aggressorID = self.robots[self.aggressorPosition].ID

        defenderID = self.robots[self.defenderPosition].ID

        return self.database.Aggressor_Can_Kill_Defender(aggressorID, defenderID)

    def Choose_Aggressor(self):

        self.aggressorPosition = random.choice( list(self.robots) )

        while self.Robot_Shown_Recently(self.aggressorPosition) or \
            self.robots[self.aggressorPosition].locked:

            self.aggressorPosition = random.choice( list(self.robots) ) 

    def Choose_Defender(self):

        self.defenderPosition = random.choice( list(self.robots) ) 

        while self.Defender_Is_Same_As_Aggressor() or \
            self.Robot_Shown_Recently(self.defenderPosition) or \
            self.robots[self.defenderPosition].locked:

            self.Choose_Aggressor()

            self.defenderPosition = random.choice( list(self.robots) ) 

    def Defender_Can_Be_Killed(self):

        self.defenderPosition = 0

        vulnerableDefenderFound = False

        while self.defenderPosition<c.popSize and not vulnerableDefenderFound:

            self.aggressorPosition = 0

            while self.aggressorPosition<c.popSize and not vulnerableDefenderFound:

                if (not self.Defender_Is_Same_As_Aggressor()) and \
                   (not self.Robot_Shown_Recently(self.aggressorPosition)) and \
                   (not self.Robot_Shown_Recently(self.defenderPosition)) and \
                   (not self.robots[self.aggressorPosition].locked) and \
                   (not self.robots[self.defenderPosition].locked) and \
                   self.Aggressor_Kills_Defender():

                    vulnerableDefenderFound = True
                else:
                    self.aggressorPosition = self.aggressorPosition + 1

            if not vulnerableDefenderFound:

                self.defenderPosition = self.defenderPosition + 1

        return vulnerableDefenderFound 

    def Defender_Is_Same_As_Aggressor(self):

        return self.defenderPosition == self.aggressorPosition

    def Delete_Robot(self, position):
        filename = "../school/students/student" + str(position) + ".p"
        print( 'Deleting ' + filename)
        os.remove(filename)

    def Determine_Simulation_Type(self):
        #Sets self.oldRobotID -1 if no robots are too old to be alive
        self.Robot_Too_Old()

        if self.Empty_Slot_In_Population():
            
            self.Simulate_Birth()
  
        elif self.oldRobotID > -1:

            self.Simulate_Death_From_Old_Age()

        elif self.User_Requested_To_See_All_Bots():

            self.Simulate_All()

        elif self.User_Requested_To_See_Best_Bot():

            self.Simulate_Best()

        else:
            self.Simulate_Competition()

    def Empty_Slot_In_Population(self):

        return len( self.robots ) < c.popSize 

    def Find_Empty_Position(self):

        positions = list( range(0,c.popSize) )

        for robotPosition in self.robots:

           positions.remove( robotPosition )

        return positions[0]
 
    def Get_Living_Robots(self):
        livingRobots = self.database.Get_Living_Robots()
        for livingRobot in livingRobots:
            self.Get_Living_Robot( livingRobot )

    def Get_Living_Robot(self,livingRobot):

        livingRobotID = self.database.From_Robot_Record_Get_ID( livingRobot)

        livingRobotPosition = self.database.From_Robot_Record_Get_Color_Index( livingRobot )

        filename = '../data/robot' + str(livingRobotID) + '.p'

        self.robots[livingRobotPosition] = pickle.load( open( filename , 'rb' ) )

    def Get_Original_Robot(self,originalRobot):

        originalRobotID = self.database.From_Robot_Record_Get_ID( originalRobot)

        originalRobotPosition = self.database.From_Robot_Record_Get_Color_Index( originalRobot )

        filename = '../data/robot' + str(originalRobotID) + '.p'

        self.originalRobots[originalRobotPosition] = pickle.load( open( filename , 'rb' ) )

    def Get_Original_Robots(self):
        originalRobots = self.database.Get_Original_Robots()
        for originalRobot in originalRobots:
            self.Get_Original_Robot( originalRobot )

    def Honor_Show_All_Request(self):

        showAllRequest = self.database.Get_Show_All_Request()

        requestID = self.database.From_Show_All_Request_Record_Get_ID(showAllRequest)

        self.database.Set_Show_All_Request_Honored(requestID)

    def Honor_Show_Best_Request(self):

        showBestRequest = self.database.Get_Show_Best_Request()

        requestID = self.database.From_Show_Best_Request_Record_Get_ID(showBestRequest)

        self.database.Set_Show_Best_Request_Honored(requestID)

    def Load_Robot(self, position):
        filename = "../school/students/student" + str(position) + ".p"
        self.robots[position] = pickle.load(open(filename, 'rb'))
        self.robots[position].Set_ID( self.database.Get_Next_Available_Robot_ID() )
        self.Delete_Robot(position)

    def Position_Is_Empty(self,robotPosition):

        return self.robots[robotPosition] == None

    def Request_To_See_All_Bots_Is_Available(self):

        showAllRequest = self.database.Get_Show_All_Request()

        if showAllRequest:

            return True

        else:

            return False
   
    def Request_To_See_Best_Bot_Is_Available(self):

        showBestRequest = self.database.Get_Show_Best_Request()

        if showBestRequest:

            return True

        else:

            return False
 
    def Retrieve_Robot_Locked_Statuses(self):

       self.Set_Robot_Locked_Statuses()

    def Robot_Available(self, position):

        filename = "../school/students/student" + str(position) + ".p"

        return os.path.isfile(filename)

    def Robot_Locked(self,robotPosition):

        robotID = self.robots[robotPosition].ID

        return self.database.Robot_Is_Locked( robotID )

    def Robot_Shown_Recently(self,robotPosition):

        robotID = self.robots[robotPosition].ID

        return self.database.Robot_Shown_Recently( robotID ) 

    #Robots can only live to be 3 days old c.deathAge
    def Robot_Too_Old(self):

        self.oldRobotID = -1

        #Calculate ages for current robots
        for robot in self.robots:
            robotInfo = self.database.Get_Robot_By_ID(self.robots[robot].Get_ID())
            lifespan = datetime.datetime.now() - robotInfo[3]
            lifespanInSeconds = lifespan.total_seconds()
            lifespanInDays = (lifespanInSeconds*1.0)/(60.0*60.0*24.0)
            if lifespanInDays >= c.deathAge:
                self.oldRobotID = self.robots[robot].Get_ID()

    def Set_Robot_Locked_Statuses(self):

       self.allBotsAreLocked = True

       for robotPosition in self.robots:

           locked = self.Robot_Locked(robotPosition)

           if locked == -1: # Robot could not be found in database

               locked = 1

           if not locked:

               self.allBotsAreLocked = False

           self.robots[robotPosition].locked = locked

    def Simulate_All(self):

        self.positionsOfRobotsBeingSimulated = []

        for robotPosition in range(0,c.popSize):
     
            self.positionsOfRobotsBeingSimulated.append( robotPosition )

        self.simulationType = c.SIMULATE_ALL

    def Simulate_All_Original_Bots(self):

        self.positionsOfRobotsBeingSimulated = []

        for robotPosition in range(0,c.popSize):

            self.positionsOfRobotsBeingSimulated.append( robotPosition )

        self.simulationType = c.SIMULATE_ALL_ORIGINAL_BOTS

    def Simulate_Best(self):

        self.positionsOfRobotsBeingSimulated = []

        bestRobotIndex , BIndex = self.database.Get_Color_Index_And_Highest_B_Index_Among_Living_Robots()

        for robotPosition in range(0,2): # Simulate the same robot for two randomly-chosen commands it obeys.
    
            self.positionsOfRobotsBeingSimulated.append( bestRobotIndex )

        self.simulationType = c.SIMULATE_BEST

    def Simulate_Birth(self):

        self.emptyPosition = self.Find_Empty_Position()

        #50/50 chance of random birth or birth from another robot, but not unless an aggressor position has been set (implying)
        if ( random.randint(0,1) == 0 or self.aggressorPosition not in self.robots):
            self.Simulate_Birth_De_Novo()
        else:
            self.Simulate_Birth_From_Aggressor()

    def Simulate_Birth_De_Novo(self):

        if (self.Robot_Available(self.emptyPosition)):

            self.Load_Robot(self.emptyPosition)
        else:
            self.robots[self.emptyPosition] = ROBOT( self.database.Get_Next_Available_Robot_ID(),
                                          colorIndex=self.emptyPosition,
                                          parentID=-1,
                                          clr=c.colorRGBs[self.emptyPosition])

        self.database.Add_Robot(self.robots[self.emptyPosition])

        self.database.Unlock_Bot( self.robots[self.emptyPosition].Get_ID() )

        self.positionsOfRobotsBeingSimulated = [ self.emptyPosition ]

        self.simulationType = c.SIMULATE_BIRTH_DE_NOVO

    def Simulate_Birth_From_Aggressor(self):

        # self.Choose_Aggressor()

        self.robots[self.emptyPosition] = copy.deepcopy(self.robots[self.aggressorPosition])

        self.robots[self.emptyPosition].Mutate()

        self.robots[self.emptyPosition].ID = self.database.Get_Next_Available_Robot_ID()

        self.robots[self.emptyPosition].colorIndex = self.emptyPosition

        self.robots[self.emptyPosition].parentID = self.robots[self.aggressorPosition].ID

        self.robots[self.emptyPosition].Set_Color(c.colorRGBs[self.emptyPosition])

        self.database.Add_Robot(self.robots[self.emptyPosition])

        self.database.Unlock_Bot( self.robots[self.emptyPosition].Get_ID() )

        self.positionsOfRobotsBeingSimulated = [ self.emptyPosition , self.aggressorPosition ]

        self.simulationType = c.SIMULATE_BIRTH_FROM_AGGRESSOR

    #Removes dying robot from robots[] and replaces it with a mutated child
    def Simulate_Death_From_Old_Age(self):
    
        self.indexOfOldRobot = -1
        for i in range(0,len(self.robots)):
            if self.robots[i].Get_ID() == self.oldRobotID:
                self.indexOfOldRobot = i

        self.oldRobotID = self.robots[self.indexOfOldRobot].Get_ID()

        self.positionsOfRobotsBeingSimulated = [ self.indexOfOldRobot ]

        self.simulationType = c.SIMULATE_DEATH_FROM_OLD_AGE

        #Making sure aggressorPosition is set to None, so that we build a robot from scratch in Simulate_Birth()
        self.aggressorPosition = None

    def Simulate_Competition(self):

        self.Retrieve_Robot_Locked_Statuses()

        if self.Defender_Can_Be_Killed():

            self.Simulate_Death()

        else:
            self.Choose_Aggressor()

            self.Choose_Defender()

            self.Simulate_Survival()

    def Simulate_Death(self):

        self.positionsOfRobotsBeingSimulated = [ self.defenderPosition , self.aggressorPosition ]

        self.simulationType = c.SIMULATE_DEATH
        

    def Simulate_Survival(self):

        self.positionsOfRobotsBeingSimulated = [ self.defenderPosition , self.aggressorPosition ]

        self.simulationType = c.SIMULATE_SURVIVAL

    def User_Requested_To_See_All_Bots(self):

        if self.Request_To_See_All_Bots_Is_Available():

           self.Honor_Show_All_Request()

           return True

        else:

           return False 

    def User_Requested_To_See_Best_Bot(self):

        if self.Request_To_See_Best_Bot_Is_Available():

           self.Honor_Show_Best_Request()

           return True

        else:

           return False
