import math
import random

import numpy as np
import constants as c

class SYNAPSE:

    def __init__(self, sourceNeuron, targetNeuron):
        self.sourceNeuron = sourceNeuron
        self.targetNeuron = targetNeuron
        self.weight = np.random.rand() * 2 - 1
        self.weight = round(self.weight, 15)
        self.Zero_Out()

    def Get_Weight(self):
        """
        :return: The weight of the synapse connection
        """
        return self.weight

    def Mutate(self):
        self.weight = random.gauss(self.weight, math.fabs(self.weight))
        self.weight = round(self.weight, 15)
        self.Zero_Out()

    def Print(self):
        print(self.weight)

    def Send_To_Simulator(self, simulator):
        if self.sourceNeuron.type == c.AUDITORY_NEURON:
            return
        simulator.send_synapse(source_neuron_id=self.sourceNeuron.ID,
                               target_neuron_id=self.targetNeuron.ID,
                               weight=self.weight)

    def Zero_Out(self):
        if (math.fabs(self.weight) < 0.5):
            self.weight = 0.0
