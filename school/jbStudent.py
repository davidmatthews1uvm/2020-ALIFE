import sys
import numpy as np
import pickle
import os.path
import math

sys.path.insert(0, '..')

import constants as c

import pyrosim.pyrosim as pyrosim

from TPR_3.robot import ROBOT

class JBSTUDENT:

    def __init__(self, ID):
        self.Initialize(ID)

    def Evaluate(self, playBlind, playPaused):
        self.Start_Evaluation(playBlind, playPaused)
        self.End_Evaluation()

    def Get_Fitness(self):
        return self.fitness

    def Get_From_Simulator(self,s):
        self.sensorData[s] = self.sims[s].wait_to_finish()

        self.Parse_Sensor_Data(s)

        del self.sims[s]

    def Is_More_Fit_Than(self, other):
        return self.fitness > other.fitness

    def Mutate(self):
        self.r.Mutate()

    def Save_And_Reset_If_Ancestor_Was_Harvested(self, ID):
        filename = "students/student" + str(ID) + ".p"

        if (os.path.isfile(filename) == False):
            self.Save(ID)
            self.Reset(ID)

    def Send_To_Simulator(self,s):
        commandEncoding = s # range: [0,c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS - 1]

        commandEncoding = commandEncoding / ( c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS - 1 ) # range: [0,1]

        self.r.Send_To_Simulator(self.sims[s], positionOffset=[0, 0, 0], drawOffset=[0, 0, 0], fadeStrategy=0,
                                 currentCommandEncoding= commandEncoding )
        self.sims[s].start()


    # ---------------------- Private methods ---------------------------------
    
    # --------------------- Fitness Functions --------------------------------
    def Compute_Fitness(self):
        self.fitness = self.Compute_Fitness_As_Distance_From_Origin()
    
    def Compute_Fitness_As_Distance_From_Origin(self):
        totalDistanceFromOriginForAllCommands = 0
        avgDistanceFromOriginForAllCommands = 0

        #Summing the distance achieved for all commands presented to the student
        for s in range(0, c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS):
            #print("XYZ sim", s, ":", self.finalPositionXYZData[s])
            #Using Pythagrian Theorum to calculate final distance
            totalDistanceFromOriginForAllCommands += math.sqrt(self.finalPositionXYZData[s][0]**2 + self.finalPositionXYZData[s][1]**2 + self.finalPositionXYZData[s][2]**2)
            #print("Total distance:", totalDistanceFromOriginForAllCommands)
        
        #Calculating the average distance among 3 command simulations
        avgDistanceFromOriginForAllCommands = totalDistanceFromOriginForAllCommands/c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS
        #print("Avg Distance:", avgDistanceFromOriginForAllCommands)

        return avgDistanceFromOriginForAllCommands

    def End_Evaluation(self):
        #Initializing dictionaries for data storage {One entry for each command (3)}
        self.InitializeDataDictionaries()

        #Get sensor data for each command simulation
        for s in range(0, c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS ):
            self.Get_From_Simulator(s)
        
        #Compute the Fitness (average fitness among 3 command simulations)
        self.Compute_Fitness()

    def Initialize(self, ID):
        self.r = ROBOT(ID=ID, colorIndex=ID, parentID=-1, clr=c.colorRGBs[ID])

        self.sims = {}

        self.sensorData = {}

        self.fitnessComponents = np.zeros( [3,c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS] , dtype='f' )

    def InitializeDataDictionaries(self):
        #Initializing dictionaries for data storage {One entry for each command (3)}
        self.touchData = {}
        self.finalPositionXYZData = {}
    
    #Organizes Data from a simulation s (total sims = num different commands a student hears)
    def Parse_Sensor_Data(self, s):
        #Record the touch sensor data for all touch sensors
        numTouchSensors = self.r.Num_Body_Parts()
        self.touchData[s] = self.sensorData[s][0:numTouchSensors, 0, 2:] #From the seceond timestep onwards?

        #Record final position vector (right pupil sensor) xyz for the final time step
        self.finalPositionXYZData[s] = self.sensorData[s][-1, 0:3, -1]

    def Reset(self, ID):
        self.Initialize(ID)
        self.Evaluate(playBlind=True, playPaused=False)

    def Save(self, ID):
        filename = "students/student" + str(ID) + ".p"
        pickle.dump(self.r, open(filename, 'wb'))

    def Start_Evaluation(self, playBlind, playPaused):

        for s in range(0, c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS ):

            self.sims[s] = pyrosim.Simulator(debug=False, play_blind=playBlind, play_paused=playPaused, eval_time=c.evaluationTime)
            self.Send_To_Simulator(s)
