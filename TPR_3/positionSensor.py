import copy

import numpy as np

import constants as c


class POSITION_SENSOR:

    def __init__(self):
        self.values = None

    def Add_Neuron(self, neurons):
        neurons.Add_Sensor_Neuron(self, c.SENSOR_NEURON)

    def Get_Data_From_Simulator(self, simulator):
        sim_x = copy.deepcopy(simulator.get_sensor_data(self.ID, svi = 0))
        sim_y = copy.deepcopy(simulator.get_sensor_data(self.ID, svi = 1))
        sim_z = copy.deepcopy(simulator.get_sensor_data(self.ID, svi = 2))

        self.values = (sim_x, sim_y, sim_z)

    def Get_Value(self):
        return np.mean(self.values)

    def Get_Values(self):
        return self.values

    def Reset_Neuron(self, neurons):
        neurons.Reset_Sensor_Neuron(self)

    def Send_To_Simulator(self, simulator, ID):
        self.ID = simulator.send_position_sensor(body_id=ID)
