import math
import random

from TPR_3.joint import JOINT
from TPR_3.object import OBJECT

import constants


class NODE:

    def __init__(self, parent, myDepth, maxDepth, numChildren, myAngle1, myAngle2, x, y, z):
        self.myDepth = myDepth
        # self.numChildren = numChildren
        self.numChildren = random.randint(1, numChildren)
        self.object = None
        self.joint = None
        self.myAngle1 = myAngle1
        self.myAngle2 = myAngle2
        self.x = x
        self.y = y
        self.z = z
        self.children = {}

        if (self.myDepth < maxDepth):
            self.Create_Children(maxDepth)
        else:
            self.numChildren = 0

    def Add_Joints(self, parent, grandParent):
        if (self.myDepth == 0):
            firstNode = self.children[0]
            secondNode = self.children[1]
            nodeContainingJointPosition = self
            q = self.children[0]
            p = self
            r = self.children[1]

            self.joint = JOINT(firstNode, secondNode, nodeContainingJointPosition, q, p, r)

        elif (self.myDepth == 1):
            self.joint = None
        else:
            firstNode = parent
            secondNode = self
            nodeContainingJointPosition = parent

            q = self
            p = parent
            r = grandParent

            self.joint = JOINT(firstNode, secondNode, nodeContainingJointPosition, q, p, r)

        for c in self.children:
            self.children[c].Add_Joints(self, parent)

    def Add_Objects(self, parent):
        if (self.myDepth == 0):
            self.object = None
        else:
            self.object = OBJECT(parent, self)

        for c in self.children:
            self.children[c].Add_Objects(self)

    def Add_Neurons(self, neurons):
        if (self.object):
            self.object.Add_Neurons(neurons)

        if (self.joint):
            self.joint.Add_Neurons(neurons)

        for c in self.children:
            self.children[c].Add_Neurons(neurons)

    def Add_Sensors(self):
        if (self.object):
            self.object.Add_Sensors()

        if (self.joint):
            self.joint.Add_Sensors()

        for c in self.children:
            self.children[c].Add_Sensors()

    def Count_Sensors(self):
        numSensors = 0

        if (self.object):
            numSensors = numSensors + self.object.Num_Sensors()

        if (self.joint):
            numSensors = numSensors + self.joint.Num_Sensors()

        for c in range(0, self.numChildren):
            numSensors = numSensors + self.children[c].Count_Sensors()

        return numSensors

    def Create_Children(self, maxDepth):
        for c in range(0, self.numChildren):
            hisAngle1 = self.myAngle1 + random.random() * 2.0 * 3.14159 - 3.14159

            hisAngle2 = math.pi / 2.0

            hisX = self.x + constants.length * math.sin(hisAngle1)

            hisY = self.y + constants.length * math.cos(hisAngle1)

            hisZ = self.z

            self.children[c] = NODE(self, self.myDepth + 1, maxDepth, constants.maxChildren, hisAngle1, hisAngle2, hisX,
                                    hisY, hisZ)

    def Find_Lowest_Point(self, lowestPoint):
        if (self.z < lowestPoint[0]):
            lowestPoint[0] = self.z

        for c in range(0, self.numChildren):
            self.children[c].Find_Lowest_Point(lowestPoint)

    def Find_Highest_Point(self, highestPoint):
        if (self.ID >= 0):
            if (self.finalZ > highestPoint[0]):
                highestPoint[0] = self.finalZ

        for c in range(0, self.numChildren):
            self.children[c].Find_Highest_Point(highestPoint)

    def First_Object(self):
        return self.children[0].object

    def Flip(self):
        self.x = -self.x

        for c in range(0, self.numChildren):
            self.children[c].Flip()

    def Get_Sensor_Data_From_Simulator(self, simulator):
        if (self.object):
            self.object.Get_Sensor_Data_From_Simulator(simulator)

        for c in range(0, self.numChildren):
            self.children[c].Get_Sensor_Data_From_Simulator(simulator)

    def Make_Parent_Of(self, other):
        other.Recalculate_Depth(self.myDepth + 1)
        self.children[self.numChildren] = other
        self.numChildren = self.numChildren + 1

    def Move(self, x, y, z):
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z

        for c in range(0, self.numChildren):
            self.children[c].Move(x, y, z)

    def Mutate(self, mutationProbability):
        mutationOccurred = False

        if (random.random() < mutationProbability):
            # self.Mutate_Length()
            self.Mutate_Angles()
            if (self.numChildren > 0):
                mutationOccurred = True

        for c in range(0, self.numChildren):
            mutationOccurred = mutationOccurred or self.children[c].Mutate(mutationProbability)

        return mutationOccurred

    def Mutate_Angles(self):
        angle1Change = random.random() * 3.14159 * 2.0 - 3.14159  # 0.1 - 0.05
        angle2Change = random.random() * 3.14159 * 2.0 - 3.14159  # 0.1 - 0.05
        self.Update_Angles(angle1Change, angle2Change)

        for c in self.children:
            self.children[c].Update_Positions(self.x, self.y, self.z)

    def Mutate_Length(self):
        self.x = self.x + random.random() * 0.1 - 0.05
        self.y = self.y + random.random() * 0.1 - 0.05
        self.z = self.z + random.random() * 0.1 - 0.05

    def Not_Moving(self):
        if (self.object):
            return self.object.Not_Moving()

        for c in self.children:
            return self.children[c].Not_Moving()

    def Number_Of_Nodes(self):
        numNodes = 1

        for c in range(0, self.numChildren):
            numNodes = numNodes + self.children[c].Number_Of_Nodes()

        return numNodes

    def Print(self):
        outputString = ''

        for i in range(0, self.myDepth):
            outputString = outputString + '   '

        # outputString = outputString + str(self.ID)

        if (self.object):
            outputString = outputString + self.object.Print()
        else:
            outputString = outputString + 'N'

        print(outputString)

        for c in range(0, self.numChildren):
            self.children[c].Print()

    def Recalculate_Depth(self, myDepth):
        self.myDepth = myDepth

        for c in range(0, self.numChildren):
            self.children[c].Recalculate_Depth(self.myDepth + 1)

    def Reset_Neurons(self, neurons):
        if (self.object):
            self.object.Reset_Neurons(neurons)

        if (self.joint):
            self.joint.Reset_Neurons(neurons)

        for c in self.children:
            self.children[c].Reset_Neurons(neurons)

    def Send_Joints_To_Simulator(self, simulator, positionOffset,initial3Dness,final3Dness):
        if (self.joint):
            self.joint.Send_To_Simulator(simulator, positionOffset,initial3Dness,final3Dness)

        for c in self.children:
            self.children[c].Send_Joints_To_Simulator(simulator, positionOffset,initial3Dness,final3Dness)

    def Send_Objects_To_Simulator(self, simulator, color, positionOffset, drawOffset, fadeStrategy):
        if (self.object):
            self.object.Send_To_Simulator(simulator, color, positionOffset, drawOffset, fadeStrategy)

        for c in self.children:
            self.children[c].Send_Objects_To_Simulator(simulator, color, positionOffset, drawOffset, fadeStrategy)

    def Send_Position_Sensors_To_Simulator(self, simulator):
        if (self.object):
            self.object.Send_Position_Sensor_To_Simulator(simulator)

        for c in self.children:
            self.children[c].Send_Position_Sensors_To_Simulator(simulator)


    def Size(self):
        size = 1

        for c in self.children:
            size = size + self.children[c].Size()

        return size

    def Sum_Light(self):
        sumOfLight = 0

        if (self.object):
            sumOfLight = self.object.Get_Light_Sensor_Value()

        for c in self.children:
            sumOfLight = sumOfLight + self.children[c].Sum_Light()

        return sumOfLight

    def Update_Angles(self, angle1Change, angle2Change):
        self.myAngle1 = self.myAngle1 + angle1Change
        self.myAngle2 = self.myAngle2 + angle2Change

        for c in self.children:
            self.children[c].Update_Angles(angle1Change, angle2Change)

    def Update_Positions(self, parentX, parentY, parentZ):
        self.x = parentX + constants.length * math.cos(self.myAngle1) * math.sin(self.myAngle2)
        self.y = parentY + constants.length * math.sin(self.myAngle1) * math.sin(self.myAngle2)
        self.z = parentZ + constants.length * math.cos(self.myAngle2)

        for c in range(0, self.numChildren):
            self.children[c].Update_Positions(self.x, self.y, self.z)
