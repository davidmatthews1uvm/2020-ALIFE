import copy
import numpy as np
import random

from TPR_3.head import HEAD
from TPR_3.node import NODE

import constants as c


class BODY:

    def __init__(self):
        self.head = None
        self.root = NODE(None, 0, c.maxDepth, 1, 0.0, 0.0, 0, 0, 0)
        self.Reset()
        self.color = [1, 1, 1]

        self.initial3Dness = c.newRobotInitial3Dness 
        self.final3Dness   = c.newRobotFinal3Dness

    def Add_Sensor_And_Motor_Neurons(self, neurons):
        self.root.Add_Neurons(neurons)
        self.head.Add_Neurons(neurons)

    def Compute_Fitness(self, whatToMaximize):
        if ( self.Not_Moving() ):
            return 0.0

        if ( whatToMaximize == c.maximizePos):
            pos = self.Get_Positions()
            if max(pos[2]) > 3:
                return 0.0
            return pos[0][-1]
        if ( whatToMaximize == c.maximizeLight ):

            return - self.Sum_Light()
        else:
            print('unknown fitness function ' + whatToMaximize)
            exit(0)

    def Get_Sensor_Data_From_Simulator(self, simulator):
        self.root.Get_Sensor_Data_From_Simulator(simulator)
        self.head.Get_Sensor_Data_From_Simulator(simulator)

    def Mutate(self):

        if random.randint(0,1) == 0:

            return self.Mutate_3DNess()

        else:
            return self.Mutate_Cylinder_Angles()

    def Not_Moving(self):
        return self.root.Not_Moving()

    def Num_Body_Parts(self):
        return self.root.Number_Of_Nodes() - 1

    def Print(self):
        self.root.Print()

    def Reset(self):
        self.Create_Mirror_Image()
        self.Add_Objects()
        self.Add_Joints()
        self.Add_Sensors()
        self.Move_Up()
        self.Add_Head()

    def Reset_Sensor_And_Motor_Neurons(self, neurons):
        self.root.Reset_Neurons(neurons)
        self.head.Reset_Neurons(neurons)

    def Send_To_Simulator(self, simulator, positionOffset, drawOffset, fadeStrategy):

        self.root.Send_Objects_To_Simulator(simulator, self.color, positionOffset, drawOffset, fadeStrategy)
        self.root.Send_Position_Sensors_To_Simulator(simulator)
        self.Send_Head_Objects(simulator, positionOffset, drawOffset, fadeStrategy)
        self.root.Send_Joints_To_Simulator(simulator, positionOffset, self.initial3Dness, self.final3Dness)
        self.Send_Head_Joints(simulator, positionOffset)
        self.Send_Head_Sensors(simulator, positionOffset, drawOffset, fadeStrategy)

    def Set_Color(self, clr):
        self.color = clr

    def Sum_Light(self):
        return self.root.Sum_Light()
        sumOfLight = 0

        if (self.lightSensor):
            sumOfLight = self.lightSensor.Get_Value()

        for c in range(0, self.numChildren):
            sumOfLight = sumOfLight + self.children[c].Sum_Light()

        return sumOfLight

    # --------------- Private methods -------------------------

    def Add_Head(self):
        self.head = HEAD(self.root.x, self.root.y, self.root.z, self.root.First_Object())

    def Add_Joints(self):
        self.root.Add_Joints(None, None)

    def Add_Objects(self):
        self.root.Add_Objects(None)

    def Add_Sensors(self):
        self.root.Add_Sensors()
        self.numSensors = self.root.Count_Sensors()

    def Create_Mirror_Image(self):
        self.root.children[1] = copy.deepcopy(self.root.children[0])
        self.root.numChildren = 2
        self.root.children[1].Flip()

    def Move_Up(self):
        lowestPoint = [1000.0]
        self.root.Find_Lowest_Point(lowestPoint)
        self.root.Move(0, 0, -lowestPoint[0] + c.eyeRadius) # c.radius)

    def Mutate_3DNess(self):

        mutType = random.randint(0,3)

        if mutType==0:       # Increase initial height

            self.initial3Dness = np.random.uniform(self.initial3Dness,self.final3Dness)

        elif mutType==1:     # Decrease initial height

            self.initial3Dness = np.random.uniform(c.minimumAmountOf3Dness,self.initial3Dness)

        elif mutType==2:     # Increase final height

            self.final3Dness = np.random.uniform(self.final3Dness,c.maximumAmountOf3Dness)

        else:                # Decrease final height

            self.final3Dness   = np.random.uniform(self.initial3Dness,self.final3Dness)

        return True

    def Mutate_Cylinder_Angles(self):

        numberOfNodes = self.root.children[0].Size()
        probabilityOfNodeMutation = 1.0 / numberOfNodes

        atLeastOneAngleGotMutated = self.root.children[0].Mutate(probabilityOfNodeMutation)

        while not atLeastOneAngleGotMutated:

            atLeastOneAngleGotMutated = self.root.children[0].Mutate(probabilityOfNodeMutation)

        return True

    def Send_Head_Joints(self, simulator, positionOffset):
        if (self.head):
            self.head.Send_Joints_To_Simulator(simulator, positionOffset)

    def Send_Head_Objects(self, simulator, positionOffset, drawOffset, fadeStrategy):
        if (self.head):
            self.head.Send_Objects_To_Simulator(simulator, positionOffset, drawOffset, fadeStrategy)

    def Send_Head_Sensors(self, simulator, positionOffset, drawOffset, fadeStrategy):
        if (self.head):
            self.head.Send_Sensors_To_Simulator(simulator, positionOffset, drawOffset)

    def Sum_Light(self):
        return self.root.Sum_Light()

    def Get_Positions(self):
        return self.head.Get_Eye_Positions()
