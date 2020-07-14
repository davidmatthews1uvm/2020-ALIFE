import random

from TPR_3.neuron import NEURON

import constants as c


class NEURONS:

    def __init__(self):
        self.s = 0
        self.sensorNeurons = {}
        self.h = 0
        self.hiddenNeurons = {}
        self.m = 0
        self.motorNeurons = {}

    def Add_Sensor_Neuron(self, sensor, type):
        self.sensorNeurons[self.s] = NEURON(type)

        if (type == c.SENSOR_NEURON):
            self.sensorNeurons[self.s].Add_Sensor_Pointer(sensor)

        self.s = self.s + 1

    def Add_Hidden_Neurons(self):
        for h in range(0, c.NUM_HIDDEN_NEURONS):
            self.hiddenNeurons[h] = NEURON(c.HIDDEN_NEURON)

            self.h = self.h + 1

    def Add_Motor_Neuron(self, joint):
        self.motorNeurons[self.m] = NEURON(c.MOTOR_NEURON)
        self.motorNeurons[self.m].Add_Joint_Pointer(joint)
        self.m = self.m + 1

    def Get_Sensor_Neuron(self, s):
        return self.sensorNeurons[s]

    def Get_Hidden_Neuron(self, h):
        return self.hiddenNeurons[h]

    def Get_Hidden_Neuron_Tau(self):
        """
        :return: a 1x5 array of the hidden neuron tau values
        """

        ret = [0]*self.h
        for i in range(self.h):
            ret[i] = self.hiddenNeurons[i].Get_Tau()
        return ret

    def Get_Motor_Neuron(self, m):
        return self.motorNeurons[m]

    def Mutate(self):
        mutType = random.randint(0, 2)

        if (mutType == 0):
            self.Mutate_Sensor_Neurons()
        elif (mutType == 1):
            self.Mutate_Hidden_Neurons()
        else:
            self.Mutate_Motor_Neurons()

    def Num_Sensor_Neurons(self):
        return self.s

    def Num_Hidden_Neurons(self):
        return self.h

    def Num_Motor_Neurons(self):
        return self.m

    def Print(self):
        self.Print_Size()
        # self.Print_Values()

    def Reset(self):
        self.newS = 0
        self.newM = 0

    def Reset_Sensor_Neuron(self, sensor):
        self.sensorNeurons[self.newS].Reset_Sensor_Pointer(sensor)
        self.newS = self.newS + 1

    def Reset_Motor_Neuron(self, joint):
        self.motorNeurons[self.newM].Reset_Joint_Pointer(joint)
        self.newM = self.newM + 1

    def Set_Hidden_Neuron_State(self, last_vals, vals):
        """
        Sets the initial internal states of the hidden neurons to support speaking a command to the robot during prenatal
        development.
        :param vals: List of current activation of hidden neurons
        :param last_vals: List of last activation of hidden neurons
        :return: None
        """
        for h in self.hiddenNeurons:
            self.hiddenNeurons[h].Set_Values(last_vals[h], vals[h])

    def Send_To_Simulator(self, simulator):
        for s in self.sensorNeurons:
            self.sensorNeurons[s].Send_Sensor_Neuron_To_Simulator(simulator)

        for h in self.hiddenNeurons:
            self.hiddenNeurons[h].Send_Hidden_Neuron_To_Simulator(simulator)

        for m in self.motorNeurons:
            self.motorNeurons[m].Send_Motor_Neuron_To_Simulator(simulator)

    # -------------------- Private functions ---------------------

    def Mutate_Sensor_Neurons(self):
        s = random.randint(0, self.Num_Sensor_Neurons() - 1)
        self.sensorNeurons[s].Mutate()

    def Mutate_Hidden_Neurons(self):
        h = random.randint(0, self.Num_Hidden_Neurons() - 1)
        self.hiddenNeurons[h].Mutate()

    def Mutate_Motor_Neurons(self):
        m = random.randint(0, self.Num_Motor_Neurons() - 1)
        self.motorNeurons[m].Mutate()

    def Print_Size(self):
        print(len(self.sensorNeurons))
        print(len(self.hiddenNeurons))
        print(len(self.motorNeurons))

    def Print_Values(self):
        for s in self.sensorNeurons:
            self.sensorNeurons[s].Print()

        for h in self.hiddenNeurons:
            self.hiddenNeurons[h].Print()

        for m in self.motorNeurons:
            self.motorNeurons[m].Print()
