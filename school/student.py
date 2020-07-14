from pyrosim.pyrosim import pyrosim

import constants as c


from TPR_3.robot import ROBOT

import numpy as np
import pickle
import os.path


class STUDENT:

    def __init__(self, ID):
        self.Initialize(ID)

    def Evaluate(self, playBlind, playPaused):
        self.Start_Evaluation(playBlind, playPaused)
        self.End_Evaluation()

    def Get_Fitness(self):
        return self.fitness

    def Get_From_Simulator(self):
        sensorData = self.s.wait_to_finish()

        self.Compute_Fitness(sensorData)

        del self.s

    def Is_More_Fit_Than(self, other):
        return self.fitness > other.fitness

    def Mutate(self):
        self.r.Mutate()

    def Save_And_Reset_If_Ancestor_Was_Harvested(self, ID):
        filename = "students/student" + str(ID) + ".p"

        if (os.path.isfile(filename) == False):
            self.Save(ID)
            self.Reset(ID)

    def Send_To_Simulator(self):
        self.r.Send_To_Simulator(self.s, positionOffset=[0, 0, 0], drawOffset=[0, 0, 0], fadeStrategy=0,
                                 currentCommandEncoding=0.0)
        self.s.start()

    # --------------------- Private methods -----------------------------------

    def Compute_Fitness(self,sensorData):

        if (self.Exploding(sensorData)):
            self.fitness = 0
            return

        self.Compute_Fitness_As_Height_Of_Eyes_And_Velocity(sensorData)

    def Compute_Fitness_As_Height_Of_Eyes_And_Velocity(self,sensorData):

        heightsOfRightPupil = sensorData[-1, 2, :]
        meanHeightOfRightPupil = np.mean(heightsOfRightPupil)

        positions = sensorData[-1, 0:3, :]

        velocities = np.fabs(positions[:, 0:c.evaluationTime - 1] - positions[:, 1:c.evaluationTime])
        sumOfVelocities = np.sum(velocities)
        self.fitness = meanHeightOfRightPupil * sumOfVelocities

    def End_Evaluation(self):
        self.Get_From_Simulator()

    def Exploding(self, sensorData):
        numTouchSensors = self.r.Num_Body_Parts()
        allTouchSensors = sensorData[0:numTouchSensors, 0, 2:]
        howManyTouchSensorsFiringAtOnce = np.sum(allTouchSensors, 0)
        timesDuringWhichNoTouchSensorsAreFiring = np.argwhere(howManyTouchSensorsFiringAtOnce == 0)
        thereIsAtLeastOneTimeStepDuringWhichNoTouchSensorsAreFiring = timesDuringWhichNoTouchSensorsAreFiring != []

        return (thereIsAtLeastOneTimeStepDuringWhichNoTouchSensorsAreFiring)

    def Initialize(self, ID):
        self.r = ROBOT(ID=ID, colorIndex=ID, parentID=-1, clr=c.colorRGBs[ID])

    def Reset(self, ID):
        self.Initialize(ID)
        self.Evaluate(playBlind=True, playPaused=False)

    def Save(self, ID):
        filename = "students/student" + str(ID) + ".p"
        pickle.dump(self.r, open(filename, 'wb'))

    def Start_Evaluation(self, playBlind, playPaused):
        self.s = pyrosim.Simulator(debug=False, play_blind=playBlind, play_paused=playPaused,
                                   eval_time=c.evaluationTime)
        self.Send_To_Simulator()
