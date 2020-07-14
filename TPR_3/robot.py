import numpy
import random


from TPR_3.body import BODY
from TPR_3.brain import BRAIN

class ROBOT:

    def __init__(self, ID, colorIndex, parentID, clr):
        self.Set_ID(ID)
        self.colorIndex = colorIndex
        self.parentID = parentID
        self.body = BODY()
        self.brain = BRAIN(self.body)
        self.Set_Color(clr)

    def Compute_Initial_State(self, cmds):
        """
        Calculates the birth state of given robot for the given command by calculating the internal states
         of the hidden neurons that should be sent to pyrosim.
        command.
        :param cmds: An iterable of iterables (Ex. a 2d array or matrix). Each object in returned by the first iterable represents a vectorized
                word in a command that may contain multiple words. Each vectorized word must be iterable as well.
        :return: A tuple where the first element is a list of the last activation state of the hidden neurons
                and the second element is the current adtivation state of the hidden neurons.
        :rtype: (numpy.ndarray, numpy.ndarray)
        """

        # create 2d Matrix of synapses, and activation states
        synapses = self.Get_Hidden_Neuron_Synapses()
        synapses_transpose = synapses.transpose() # We need to compute the transpose for calculating the dot product

        # get the tau values
        taus = self.Get_Hidden_Neuron_Tau()

        # get the alpha values. Currently these are all 1
        # Note: Multiplying two numpy 1D arrays will work if either one is a 1x1 array,
        # or if they are both the same shape. Either element-wise multiplication, or multiply the 1x1 element with all
        # elements in the other array.
        alphas = numpy.array([1])

        current_activations = numpy.zeros(5)
        last_activations = numpy.zeros(5)
        inputs = numpy.zeros(6)                 # 5 hidden neurons + 1 auditory neuron for input to 5 hidden neurons.

        for cmd in cmds:
            if isinstance(cmd, float):
                cmd = [cmd]
            for val in cmd:
                last_activations = current_activations      # keep track of last activation states
                inputs[0:5] = current_activations           # update the new inputs
                inputs[-1:] = val
                activation = numpy.dot(synapses_transpose, inputs)

                current_activations = numpy.tanh(alphas * activation + taus * last_activations)# update the current activation states

        return (last_activations, current_activations)

    def Evaluate(self, simulator, whatToMaximize):
        self.body.Get_Sensor_Data_From_Simulator(simulator)

        return self.body.Compute_Fitness(whatToMaximize)

    def Get_Hidden_Neuron_Synapses(self):
        """
        :return: 6x5 matrix of the hidden synapses. Each row column represents a hidden neuron. Each row represents
                that specific hidden neuron's synapse weights to the other hidden neurons and the auditory neuron.
                The last row is the hidden neuron to auditory neuron synapse weights.
        """
        return self.brain.Get_Hidden_Neuron_Synapses()


    def Get_Hidden_Neuron_Tau(self):
        """
        :return: a 1x5 matrix of the hidden neuron tau values.
        """
        return self.brain.Get_Hidden_Neuron_Tau()
 
    def Get_ID(self):

        return self.ID

    def Mutate(self):
        mutType = random.randint(0, 1)

        if (mutType == 0):
        
            mutateBody = self.body.Mutate()

        else:
            self.brain.Mutate()
            mutateBody = False

        self.Reset()

        return mutateBody

    def Num_Body_Parts(self):
        return self.body.Num_Body_Parts()

    def Num_Joints(self):
        return self.body.numJoints

    def Num_Neurons(self):
        return self.brain.numNeurons

    def Num_Sensors(self):
        return self.body.numSensors

    def Preform_Prenatal_Development(self, encoding):
        """
        Preforms prenatal development for a given robot by updating the brain of the robot to store the initial internal
        states of the hidden neurons to allow robots to enter the pyrosim simulation engine having already heard the
        command.
        :param encoding: An iterable of iterables (Ex. a 2d array or matrix). Each object in returned by the first iterable represents a vectorized
                word in a command that may contain multiple words. Each vectorized word must be iterable as well.
        :return: None
        """
        #Each object returned by the encoding also needs to be iterable. Ex. A 2d array or matrix. This is not checked here.
        assert hasattr(encoding, "__iter__"), "encoding must be iterable. Recieved: " + str(type(encoding))

        # compute the initial internal state of the hidden neurons
        initial_state = self.Compute_Initial_State(encoding)

        # update the internal states of the hidden neurons
        self.Set_Hidden_Neuron_State(initial_state[0], initial_state[1])

    def Print(self):
        self.body.Print()
        self.brain.Print()

    def Reset(self):
        self.body.Reset()
        self.brain.Reset(self.body)

    def Set_Hidden_Neuron_State(self, last_vals, vals):
        """
        Sets the initial internal states of the hidden neurons to support speaking a command to the robot during prenatal
        development.
        :param vals: List of current activation of hidden neurons
        :param last_vals: List of last activation of hidden neurons
        :return: None
        """
        self.brain.Set_Hidden_Neuron_State(last_vals, vals)

    def Send_To_Simulator(self, simulator, positionOffset, drawOffset, fadeStrategy, currentCommandEncoding):
        """
        Takes a robot and a command, preforms the prenatal development of the robot using numpy and then sends the
        developed robot to the simulator to be simulated.

        :param simulator: A pyrosim simulation engine
        :type simulator: A pyrosim.Simulator
        :param positionOffset:
        :param drawOffset:
        :param fadeStrategy:
        :param currentCommandEncoding: The vectorized format of the command to send to the robot.
        :type currentCommandEncoding: int, float, or must be iterable (ex. list, tuple). If the currentCommandEncoding
                is iterable, then each of the elements of the currentCommandEncoding must also be iterable ( ex. 2d array)
        :return: None
        """

        # For backwards compatability, we still support int and floats. These next few lines convert old style command encodings
        # to current command encodings to allow for support with prenatal development.

        encoding = None
        if isinstance(currentCommandEncoding, int) or isinstance(currentCommandEncoding, float):
            encoding = [[currentCommandEncoding]]
        else:
            encoding = currentCommandEncoding

        self.Preform_Prenatal_Development(encoding)

        self.body.Send_To_Simulator(simulator, positionOffset, drawOffset, fadeStrategy)
        self.brain.Send_To_Simulator(simulator)

    def Set_Color(self, clr):
        self.body.Set_Color(clr)

    def Set_ID(self, ID):
        self.ID = ID
