import math

from TPR_3.touchSensor import TOUCH_SENSOR
from TPR_3.positionSensor import POSITION_SENSOR

import constants as c


class OBJECT:

    def __init__(self, parentNode, childNode):
        self.parent = parentNode
        self.child = childNode
        self.lightSensor = None
        self.touchSensor = None
        self.positionSensor = None

    def Add_Neurons(self, neurons):
        if (self.touchSensor):
            self.touchSensor.Add_Neuron(neurons)

        if (self.lightSensor):
            self.lightSensor.Add_Neuron(neurons)

    def Add_Sensors(self):
        self.touchSensor = TOUCH_SENSOR(object=self)
        self.positionSensor = POSITION_SENSOR()

        # self.lightSensor = LIGHT_SENSOR( object = self )

    def Get_Light_Sensor_Value(self):
        if (self.lightSensor):
            return self.lightSensor.Get_Mean_Value()
        else:
            return 0

    def Get_Sensor_Data_From_Simulator(self, simulator):
        if (self.lightSensor):
            self.lightSensor.Get_Data_From_Simulator(simulator)

        if (self.touchSensor):
            self.touchSensor.Get_Data_From_Simulator(simulator)

    def Not_Moving(self):
        if (self.lightSensor):
            return self.lightSensor.Not_Moving()
        else:
            return True

    def Num_Sensors(self):
        numSensors = 0

        if (self.touchSensor):
            numSensors = numSensors + 1

        if (self.lightSensor):
            numSensors = numSensors + 1

        return numSensors

    def Print(self):
        outputString = ''

        return outputString

    def Reset_Neurons(self, neurons):
        if (self.touchSensor):
            self.touchSensor.Reset_Neuron(neurons)

        if (self.lightSensor):
            self.lightSensor.Reset_Neuron(neurons)

    def Send_Position_Sensor_To_Simulator(self, simulator):
        """
        If a position sensor is associated with this robot, it will be sent to the simulator.
        :param simulator: the pyrosim SIMULATOR being used for simulation
        :return: None
        """
        if self.positionSensor:
            self.positionSensor.Send_To_Simulator(simulator, self.ID)

    def Send_To_Simulator(self, simulator, color, positionOffset, drawOffset, fadeStrategy):
        x = (self.parent.x + self.child.x) / 2.0 + positionOffset[0]
        y = (self.parent.y + self.child.y) / 2.0 + positionOffset[1]
        z = (self.parent.z + self.child.z) / 2.0 + positionOffset[2]

        r1 = self.child.x - self.parent.x
        r2 = self.child.y - self.parent.y
        r3 = self.child.z - self.parent.z

        xDiff = self.child.x - self.parent.x
        yDiff = self.child.y - self.parent.y
        zDiff = self.child.z - self.parent.z

        length = math.sqrt(math.pow(xDiff, 2.0) + math.pow(yDiff, 2.0) + pow(zDiff, 2.0))

        if not (self.parent.myDepth==0 and self.child.myDepth==1):
 
            self.ballID = simulator.send_cylinder(x=self.parent.x+positionOffset[0], y=self.parent.y+positionOffset[1], z=self.parent.z+positionOffset[2],
                                              length=0, radius=0.5*c.radius,
                                              draw_offset_x=drawOffset[0], draw_offset_y=drawOffset[1], draw_offset_z=drawOffset[2],
                                              r=color[0], g=color[1], b=color[2],
                                              fade_strategy=fadeStrategy,
                                              capped=True,
                                              collision_group='robot')
        else:
            self.ballID = None

        self.ID = simulator.send_cylinder(x=x, y=y, z=z,
                                          r1=r1, r2=r2, r3=r3,
                                          length=length, radius=c.radius,
                                          draw_offset_x=drawOffset[0], draw_offset_y=drawOffset[1], draw_offset_z=drawOffset[2],
                                          r=color[0], g=color[1], b=color[2],
                                          fade_strategy=fadeStrategy,
                                          capped=True,
                                          collision_group='robot')

        # if ( self.lightSensor ):
        #       self.lightSensor.Send_To_Simulator(simulator)

        if (self.touchSensor):
            self.touchSensor.Send_To_Simulator(simulator)
