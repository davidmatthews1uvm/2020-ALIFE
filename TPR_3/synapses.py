import random
import numpy


from TPR_3.synapse import SYNAPSE
import constants as c

class SYNAPSES:

    def __init__(self, neurons):
        self.Create_SH(neurons)
        self.Create_HH(neurons)
        self.Create_HM(neurons)

    def Mutate(self):
        mutType = random.randint(0, 2)

        if (mutType == 0):
            self.Mutate_SH()
        elif (mutType == 1):
            self.Mutate_HH()
        else:
            self.Mutate_HM()

    def Print(self):
        self.Print_Size()
        # self.Print_Values()

    def Reset(self, neuronsCreated):
        self.Update_SH(neuronsCreated)
        self.Update_HH(neuronsCreated)
        self.Update_HM(neuronsCreated)

    def Send_To_Simulator(self, simulator):
        self.Send_SH(simulator)
        self.Send_HH(simulator)
        self.Send_HM(simulator)




    # -------------------- Private functions ---------------------

    def Create_SH(self, neurons):
        self.sh = {}

        for s in range(0, neurons.Num_Sensor_Neurons()):

            for h in range(0, neurons.Num_Hidden_Neurons()):
                sourceNeuron = neurons.Get_Sensor_Neuron(s)
                targetNeuron = neurons.Get_Hidden_Neuron(h)
                self.sh[s, h] = SYNAPSE(sourceNeuron, targetNeuron)

    def Create_HH(self, neurons):
        self.hh = {}

        for h1 in range(0, neurons.Num_Hidden_Neurons()):
            for h2 in range(0, neurons.Num_Hidden_Neurons()):
                sourceNeuron = neurons.Get_Hidden_Neuron(h1)
                targetNeuron = neurons.Get_Hidden_Neuron(h2)
                self.hh[h1, h2] = SYNAPSE(sourceNeuron, targetNeuron)

    def Create_HM(self, neurons):
        self.hm = {}

        for h in range(0, neurons.Num_Hidden_Neurons()):
            for m in range(0, neurons.Num_Motor_Neurons()):
                sourceNeuron = neurons.Get_Hidden_Neuron(h)
                targetNeuron = neurons.Get_Motor_Neuron(m)
                self.hm[h, m] = SYNAPSE(sourceNeuron, targetNeuron)

    def Get_Hidden_Neuron_Synapses(self):
        """
        :return: 6x5 matrix of the hidden synapses. Each row column represents a hidden neuron. Each row represents
                that specific hidden neuron's synapse weights to the other hidden neurons and the auditory neuron.
                The last row is the hidden neuron to auditory neuron synapse weights.
        """
        synapses = numpy.zeros((6, 5))

        # store hidden-hidden synapse weights.
        for h1, h2 in self.hh:
            synapses[h2, h1] = self.hh[h1, h2].Get_Weight()

        # store hidden-auditory synapse weights.
        for s, h in self.sh:
            if self.sh[s, h].sourceNeuron.type == c.AUDITORY_NEURON:
                synapses[5, h] = self.sh[s, h].Get_Weight()

        return synapses
    def Mutate_SH(self):
        s, h = random.choice(list(self.sh.keys()))
        self.sh[s, h].Mutate()

    def Mutate_HH(self):
        h1, h2 = random.choice(list(self.hh.keys()))
        self.hh[h1, h2].Mutate()

    def Mutate_HM(self):
        h, m = random.choice(list(self.hm.keys()))
        self.hm[h, m].Mutate()

    def Print_Size(self):
        print(len(self.sh))
        print(len(self.hh))
        print(len(self.hm))

    def Print_Values(self):
        self.Print_SH()
        self.Print_HH()
        self.Print_HM()

    def Print_SH(self):
        for s, h in self.sh:
            self.sh[s, h].Print()

    def Print_HH(self):
        for h1, h2 in self.hh:
            self.hh[h1, h2].Print()

    def Print_HM(self):
        for h, m in self.hm:
            self.hm[h, m].Print()

    def Send_SH(self, simulator):
        for s, h in self.sh:
            self.sh[s, h].Send_To_Simulator(simulator)

    def Send_HH(self, simulator):
        for h1, h2 in self.hh:
            self.hh[h1, h2].Send_To_Simulator(simulator)

    def Send_HM(self, simulator):
        for h, m in self.hm:
            self.hm[h, m].Send_To_Simulator(simulator)
