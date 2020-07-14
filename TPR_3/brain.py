import random

from TPR_3.neurons import NEURONS
from TPR_3.synapses import SYNAPSES


class BRAIN:

    def __init__(self, body):
        self.neurons = NEURONS()
        body.Add_Sensor_And_Motor_Neurons(self.neurons)
        self.neurons.Add_Hidden_Neurons()
        self.synapses = SYNAPSES(self.neurons)

    def Mutate(self):
        mutType = random.randint(0, 1)

        if (mutType == 0):
            self.neurons.Mutate()
        else:
            self.synapses.Mutate()

    def Reset(self, body):
        self.Reset_Neurons(body)

    def Get_Hidden_Neuron_Tau(self):
        """
        :return: a 1x5 array of the hidden neuron tau values.
        """
        return self.neurons.Get_Hidden_Neuron_Tau()

    def Get_Hidden_Neuron_Synapses(self):
        """
        :return: 6x5 matrix of the hidden synapses. Each row column represents a hidden neuron. Each row represents
                that specific hidden neuron's synapse weights to the other hidden neurons and the auditory neuron.
                The last row is the hidden neuron to auditory neuron synapse weights.
        """
        return self.synapses.Get_Hidden_Neuron_Synapses()

    def Set_Hidden_Neuron_State(self, last_vals, vals):
        """
        Sets the initial internal states of the hidden neurons to support speaking a command to the robot during prenatal
        development.
        :param vals: List of current activation of hidden neurons
        :param last_vals: List of last activation of hidden neurons
        :return: None
        """

        self.neurons.Set_Hidden_Neuron_State(last_vals, vals)

    def Send_To_Simulator(self, simulator):
        self.neurons.Send_To_Simulator(simulator)
        self.synapses.Send_To_Simulator(simulator)

    # ----------------- Private methods -----------------------

    def Print(self):
        self.neurons.Print()
        self.synapses.Print()

    def Reset_Neurons(self, body):
        self.neurons.Reset()
        body.Reset_Sensor_And_Motor_Neurons(self.neurons)
