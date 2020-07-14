import math
import numpy as np
from TPR_3.proprioceptiveSensor import PROPRIOCEPTIVE_SENSOR

import constants as c


class JOINT:

    def __init__(self, firstNode, secondNode, nodeWithMyPosition, q, p, r):
        self.firstNode = firstNode
        self.secondNode = secondNode
        self.nodeWithMyPosition = nodeWithMyPosition
        self.proprioceptiveSensor = None
        self.q = q
        self.p = p
        self.r = r

    def Add_Neurons(self, neurons):
        if (self.proprioceptiveSensor):
            self.proprioceptiveSensor.Add_Neuron(neurons)

        neurons.Add_Motor_Neuron(self)

    def Add_Sensors(self):
        if (self.firstNode.object and self.secondNode.object):
            self.proprioceptiveSensor = PROPRIOCEPTIVE_SENSOR(joint=self)

    def Num_Sensors(self):
        numSensors = 0

        if (self.proprioceptiveSensor):
            numSensors = numSensors + 1

        return numSensors

    def Reset_Neurons(self, neurons):
        if (self.proprioceptiveSensor):
            self.proprioceptiveSensor.Reset_Neuron(neurons)

        neurons.Reset_Motor_Neuron(self)

    def Print(self):
        outputString = ''
        outputString = outputString + str(self.ID)

        return outputString

    def Send_To_Simulator(self, simulator, positionOffset,initial3Dness,final3Dness):

        firstObjectID = self.firstNode.object.ID
        secondObjectID = self.secondNode.object.ID

        x = self.nodeWithMyPosition.x + positionOffset[0]
        y = self.nodeWithMyPosition.y + positionOffset[1]
        z = self.nodeWithMyPosition.z + positionOffset[2]
        n = self.Compute_Joint_Normal()
        n[0] = 0
        n[1] = 0
        n[2] = 1

        lo = -c.JOINT_ANGLE_MAX
        hi = +c.JOINT_ANGLE_MAX

        if self.secondNode.object.ballID:

            self.ID = simulator.send_hinge_joint(first_body_id=self.firstNode.object.ID,
                                                 second_body_id=self.secondNode.object.ballID,
                                                 x=x, y=y, z=z,
                                                 n1=n[0], n2=n[1], n3=n[2],
                                                 lo=lo, hi=hi)

            self.Add_Ball_ID(simulator,x,y,z,initial3Dness,final3Dness)

        else:
            self.ID = simulator.send_hinge_joint(first_body_id=self.firstNode.object.ID,
                                                 second_body_id=self.secondNode.object.ID,
                                                 x=x, y=y, z=z,
                                                 n1=n[0], n2=n[1], n3=n[2],
                                                 lo=lo, hi=hi)

        if (self.proprioceptiveSensor):
            self.proprioceptiveSensor.Send_To_Simulator(simulator)

    # -------------------------- Private methods ----------------------------------

    def Add_Ball_ID(self,simulator,x,y,z,initial3Dness,final3Dness):

        myFinalAngle = self.secondNode.myAngle2

        vectorDescribingFirstCylinderx  = self.q.x - self.p.x
        vectorDescribingFirstCylindery  = self.q.y - self.p.y
        vectorDescribingFirstCylinderz  = self.q.z - self.p.z

        vectorDescribingSecondCylinderx = self.r.x - self.p.x
        vectorDescribingSecondCylindery = self.r.y - self.p.y
        vectorDescribingSecondCylinderz = self.r.z - self.p.z

        myN = np.zeros(3,dtype='f')

        myN[0] = ( vectorDescribingFirstCylinderx + vectorDescribingSecondCylinderx ) / 2
        myN[1] = ( vectorDescribingFirstCylindery + vectorDescribingSecondCylindery ) / 2
        myN[2] = ( vectorDescribingFirstCylinderz + vectorDescribingSecondCylinderz ) / 2

        myN = myN / np.linalg.norm(myN)

        self.ballID = simulator.send_hinge_joint(first_body_id=self.secondNode.object.ballID,
                                             second_body_id=self.secondNode.object.ID,
                                             x=x, y=y, z=z,
                                             n1=myN[0], n2=myN[1], n3=myN[2],
                                             lo=-math.pi/2.,hi=+math.pi/2.)
                                             # lo=myFinalAngle, hi=myFinalAngle)
  
        if self.nodeWithMyPosition.x < 0: # Left side of body...

            amountsOf3Dness = np.linspace( start = +initial3Dness , stop = +final3Dness ,num=c.evaluationTime)

        else:
            amountsOf3Dness = np.linspace( start = -initial3Dness , stop = -final3Dness ,num=c.evaluationTime)

        inputNeuronID = simulator.send_user_input_neuron( in_values = amountsOf3Dness )

        motorNeuronID = simulator.send_motor_neuron( joint_id = self.ballID , tau = 1.0 , alpha = 0.0 )

        simulator.send_synapse( source_neuron_id=inputNeuronID, target_neuron_id=motorNeuronID, weight=1.0 )

    def Compute_Joint_Normal(self):
        P = np.zeros(3)
        P[0] = self.p.x
        P[1] = self.p.y
        P[2] = self.p.z

        Q = np.zeros(3)
        Q[0] = self.q.x
        Q[1] = self.q.y
        Q[2] = self.q.z

        R = np.zeros(3)
        R[0] = self.r.x
        R[1] = self.r.y
        R[2] = self.r.z

        a = Q - P
        b = R - P

        return np.cross(a, b)

    def Is_At_Top_Of_Body(self):

        return ( self.firstNode.myDepth == 1 ) and ( self.secondNode.myDepth == 1 )
