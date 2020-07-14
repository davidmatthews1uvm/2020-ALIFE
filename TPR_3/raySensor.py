import copy

import numpy as np

import constants as c


class RAY_SENSOR:

    def __init__(self):
        pass

    def Add_Neuron(self, neurons):
        neurons.Add_Sensor_Neuron(self, c.SENSOR_NEURON)

    def Get_Data_From_Simulator(self, simulator):

        self.values = copy.deepcopy(simulator.get_sensor_data(self.ID, 0))

    def Get_Value(self):
        return np.mean(self.values)

    def Reset_Neuron(self, neurons):
        neurons.Reset_Sensor_Neuron(self)

    def Send_To_Simulator(self, simulator, ID, x, y, z, drawOffset):
        self.ID = simulator.send_ray_sensor(body_id=ID,
                                            x=x,
                                            y=y,
                                            z=z,
                                            draw_offset_x=drawOffset[0],
                                            draw_offset_y=drawOffset[1],
                                            draw_offset_z=drawOffset[2],
                                            r1=0, r2=-1, r3=0)
