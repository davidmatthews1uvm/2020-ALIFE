import copy
import math

import numpy as np

import constants as c


class LIGHT_SENSOR:

    def __init__(self, object):
        self.object = object

    def Add_Neuron(self, neurons):
        neurons.Add_Sensor_Neuron(self, c.SENSOR_NEURON)

    def Get_Data_From_Simulator(self, simulator):
        self.values = copy.deepcopy(simulator.Get_Sensor_Data(self.ID, 0))

    def Get_Mean_Value(self):
        return np.mean(self.values)

    def Not_Moving(self):
        return (math.fabs(self.values[-1] - self.values[-2]) == 0)

    def Reset_Neuron(self, neurons):
        neurons.Reset_Sensor_Neuron(self)

    def Send_To_Simulator(self, simulator):
        self.ID = simulator.send_light_sensor(body_id=self.object.ID)
