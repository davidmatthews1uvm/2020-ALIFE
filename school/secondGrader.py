import sys
import numpy as np
import pickle
import os.path

sys.path.insert(0, '..')

import constants as c

import pyrosim.pyrosim as pyrosim

from TPR_3.robot import ROBOT


class STUDENT:

    def __init__(self, ID):
        self.Initialize(ID)

    def Evaluate(self, playBlind, playPaused):
        self.Start_Evaluation(playBlind, playPaused)
        self.End_Evaluation()

    def Get_Fitness(self):
        return self.fitness

    def Get_From_Simulator(self,s):
        self.sensorData[s] = self.sims[s].wait_to_finish()

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

    # --------------------- Private methods -----------------------------------

    def Maximize_Variance_In_Height_Of_Head(self):

        for s in range(0, c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS ):

            rightPupilPositionSensor = -1

            z = 2

            lastTimeStep = -1

            heightOfRightPupilAtLastTimeStep = self.sensorData[s][rightPupilPositionSensor , z , lastTimeStep]

            self.fitnessComponents[s] = heightOfRightPupilAtLastTimeStep

        standardDeviationsForZ = np.std( self.fitnessComponents )

        return standardDeviationsForZ

    def Compute_Fitness(self):

        self.fitness = self.Maximize_Variance_In_Height_Of_Head()

    def End_Evaluation(self):

        for s in range(0, c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS ):

            self.Get_From_Simulator(s)

        for s in range(0, c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS ):

            self.Compute_Fitness()

    def Exploding(self, sensorData):
        numTouchSensors = self.r.Num_Body_Parts()
        #Get the 0th sensor (touch), svi = 0 (there's only 1 index for touch), every other?
        allTouchSensors = sensorData[0:numTouchSensors, 0, 2:] 
        howManyTouchSensorsFiringAtOnce = np.sum(allTouchSensors, 0)
        timesDuringWhichNoTouchSensorsAreFiring = np.argwhere(howManyTouchSensorsFiringAtOnce == 0)
        thereIsAtLeastOneTimeStepDuringWhichNoTouchSensorsAreFiring = timesDuringWhichNoTouchSensorsAreFiring != []

        return (thereIsAtLeastOneTimeStepDuringWhichNoTouchSensorsAreFiring)

    def Initialize(self, ID):
        self.r = ROBOT(ID=ID, colorIndex=ID, parentID=-1, clr=c.colorRGBs[ID])

        self.sims = {}

        self.sensorData = {}

        self.fitnessComponents = np.zeros( [3,c.NUM_DIFFERENT_COMMANDS_A_STUDENT_HEARS] , dtype='f' )

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
