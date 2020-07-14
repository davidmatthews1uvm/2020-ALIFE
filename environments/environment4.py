import math

class ENVIRONMENT4:

    def __init__(self, simulator):
        self.simulator = simulator

        self.armLength = 2 
        self.armWidth  = 0.1
        self.armHeight = self.armWidth

    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = 0

        return x, y, z

    def Send_To_Simulator(self,positionOffset, drawOffset, fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        numArms = 5

        for self.armIndex in range(0,numArms):

            self.Send_Arm()

            self.Send_Hinge()

    # --------------- Private functions -----------------------------------------------------

    def Send_Arm(self):
        x = -self.armLength / 2   + self.positionOffset[0]
        y = self.armIndex         + self.positionOffset[1]
        z = 1.05 * self.armLength + self.positionOffset[2]

        # The 1.05 moves the arm up a bit and ensures it does not hit the ground. 

        self.armID = self.simulator.send_box(x=x, y=y, z=z,
                                          length = self.armWidth,
                                          width  = self.armLength, 
                                          height = self.armHeight,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env')

    def Send_Hinge(self):

        x = 0                       + self.positionOffset[0]
        y = self.armIndex           + self.positionOffset[1]
        z = 1.05 * self.armLength   + self.positionOffset[2]

        # The 1.05 moves the arm up a bit and ensures it does not hit the ground.

        self.hingeID = self.simulator.send_hinge_joint(first_body_id  = -1, 
                                                       second_body_id = self.armID, 
                                                       x =x, y =y, z =z,
                                                       n1=0, n2=1, n3=0,
                                                       lo=-math.pi,
                                                       hi=+math.pi)
                                                       #speed=1.0, torque=10.0, position_control=True)
