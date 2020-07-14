import constants as c

from TPR_3.positionSensor import POSITION_SENSOR
from TPR_3.raySensor import RAY_SENSOR



class HEAD:

    def __init__(self, x, y, z, objectToAttachEyesTo):
        self.x = x
        self.leftEyeX = x - c.eyeRadius * 0.67
        self.rightEyeX = x + c.eyeRadius * 0.67
        self.y = y
        self.pupilY = y - c.eyeRadius * 0.67
        self.beamY = self.pupilY - c.pupilRadius
        self.z = z # + c.eyeRadius
        self.objectToAttachEyesTo = objectToAttachEyesTo
        self.lo = 0  # -0.1
        self.hi = 0  # +0.1
        self.Initialize_Sensors()

    def Add_Neurons(self, neurons):
        neurons.Add_Sensor_Neuron(self.leftRaySensor, c.SENSOR_NEURON)
        neurons.Add_Sensor_Neuron(self.rightRaySensor, c.SENSOR_NEURON)
        neurons.Add_Sensor_Neuron(sensor=None, type=c.AUDITORY_NEURON)
        neurons.Add_Motor_Neuron(self)

    def Initialize_Sensors(self):
        self.leftRaySensor = RAY_SENSOR()
        self.rightRaySensor = RAY_SENSOR()
        self.rightEyePositionSensor = POSITION_SENSOR()
        self.leftEyePositionSensor = POSITION_SENSOR()

    def Reset_Neurons(self, neurons):
        neurons.Reset_Sensor_Neuron(self.leftRaySensor)
        neurons.Reset_Sensor_Neuron(self.rightRaySensor)
        neurons.Reset_Sensor_Neuron(self.rightEyePositionSensor)
        neurons.Reset_Motor_Neuron(self)

    def Get_Sensor_Data_From_Simulator(self, simulator):
        self.rightEyePositionSensor.Get_Data_From_Simulator(simulator)
        self.leftEyePositionSensor.Get_Data_From_Simulator(simulator)
        self.rightRaySensor.Get_Data_From_Simulator(simulator)
        self.leftRaySensor.Get_Data_From_Simulator(simulator)

    def Get_Head_Positions(self):
        return self.rightEyePositionSensor.Get_Values()

    def Get_Eye_Positions(self):
        return (self.leftEyePositionSensor.Get_Values(), self.rightEyePositionSensor.Get_Values())

    def Send_Joints_To_Simulator(self, simulator, positionOffset):
        # x = self.leftEyeX + positionOffset[0]
        x = self.x + positionOffset[0]
        y = self.y + positionOffset[1]
        z = self.z + positionOffset[2]

        self.ID = self.leftEyeJoint = simulator.send_hinge_joint(first_body_id=self.leftEye,
                                                                 second_body_id=self.objectToAttachEyesTo.ID,
                                                                 x=x, y=y, z=z,
                                                                 n1=0, n2=0, n3=1,
                                                                 lo=- c.MAX_HEAD_ROTATION,
                                                                 hi=+ c.MAX_HEAD_ROTATION)

        x = self.rightEyeX + positionOffset[0]

        self.rightEyeJoint = simulator.send_hinge_joint(first_body_id=self.rightEye,
                                                        second_body_id=self.leftEye,
                                                        # self.objectToAttachEyesTo.ID,
                                                        x=x, y=y, z=z,
                                                        n1=0, n2=0, n3=1,
                                                        lo=self.lo, hi=self.hi)

        x = self.leftEyeX + positionOffset[0]
        y = self.pupilY + positionOffset[1]

        self.leftPupilJoint = simulator.send_hinge_joint(first_body_id=self.leftPupil,
                                                         second_body_id=self.leftEye,
                                                         x=x, y=y, z=z,
                                                         n1=0, n2=0, n3=1,
                                                         lo=self.lo, hi=self.hi)

        x = self.rightEyeX + positionOffset[0]

        self.rightPupilJoint = simulator.send_hinge_joint(first_body_id=self.rightPupil,
                                                          second_body_id=self.rightEye,
                                                          x=x, y=y, z=z,
                                                          n1=0, n2=0, n3=1,
                                                          lo=self.lo, hi=self.hi)

    def Send_Objects_To_Simulator(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = self.leftEyeX + positionOffset[0]
        y = self.y + positionOffset[1]
        z = self.z + positionOffset[2]

        self.leftEye = simulator.send_cylinder(x=x, y=y, z=z,
                                               length=0, radius=c.eyeRadius,
                                               draw_offset_x=drawOffset[0],
                                               draw_offset_y=drawOffset[1],
                                               draw_offset_z=drawOffset[2],
                                               fade_strategy=fadeStrategy,
                                               r=1, g=1, b=1)

        x = self.rightEyeX + positionOffset[0]

        self.rightEye = simulator.send_cylinder(x=x, y=y, z=z,
                                                length=0, radius=c.eyeRadius,
                                                draw_offset_x=drawOffset[0],
                                                draw_offset_y=drawOffset[1],
                                                draw_offset_z=drawOffset[2],
                                                fade_strategy=fadeStrategy,
                                                r=1, g=1, b=1)

        x = self.leftEyeX + positionOffset[0]
        y = self.pupilY + positionOffset[1]

        self.leftPupil = simulator.send_cylinder(x=x, y=y, z=z,
                                                 length=0, radius=c.pupilRadius,
                                                 draw_offset_x=drawOffset[0],
                                                 draw_offset_y=drawOffset[1],
                                                 draw_offset_z=drawOffset[2],
                                                 fade_strategy=fadeStrategy,
                                                 r=0, g=0, b=0)

        x = self.rightEyeX + positionOffset[0]

        self.rightPupil = simulator.send_cylinder(x=x, y=y, z=z,
                                                  length=0, radius=c.pupilRadius,
                                                  draw_offset_x=drawOffset[0],
                                                  draw_offset_y=drawOffset[1],
                                                  draw_offset_z=drawOffset[2],
                                                  fade_strategy=fadeStrategy,
                                                  r=0, g=0, b=0)
        # simulator.film_body(self.rightPupil, method='follow')

    def Send_Sensors_To_Simulator(self, simulator, positionOffset, drawOffset):
        x = self.leftEyeX + positionOffset[0]
        y = self.beamY + positionOffset[1]
        z = self.z + positionOffset[2]

        self.leftRaySensor.Send_To_Simulator(simulator, self.leftPupil, x, y, z, drawOffset)

        x = self.rightEyeX + positionOffset[0]

        self.rightRaySensor.Send_To_Simulator(simulator, self.rightPupil, x, y, z, drawOffset)
        self.leftEyePositionSensor.Send_To_Simulator(simulator, self.leftPupil)
        self.rightEyePositionSensor.Send_To_Simulator(simulator, self.rightPupil)


