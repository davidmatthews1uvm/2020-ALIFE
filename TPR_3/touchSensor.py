import copy

import numpy as np

import constants as c


class TOUCH_SENSOR:

    def __init__(self, object):
        self.object = object
        self.values = None

    def Add_Neuron(self, neurons):
        neurons.Add_Sensor_Neuron(self, c.SENSOR_NEURON)

    def Get_Data_From_Simulator(self, simulator):
        self.values = copy.deepcopy(simulator.get_sensor_data(self.ID, 0))

    def Get_Value(self):
        return np.mean(self.values)

    def Reset_Neuron(self, neurons):
        neurons.Reset_Sensor_Neuron(self)

    def Send_To_Simulator(self, simulator):
        self.ID = simulator.send_touch_sensor(body_id=self.object.ID)
