import math

class ENVIRONMENT9:

    def __init__(self, simulator):
        self.simulator = simulator

        self.baseRadius = 0.05

        self.platformHeight = self.baseRadius * 2
 
        self.platformWidth  = 1.5
        self.platformLength = 0.5
 
    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = 1

        return x, y, z

    def Send_To_Simulator(self,positionOffset, drawOffset, fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        self.Send_Base()

        self.Send_Platform()

        self.Send_Hinge()

    # --------------- Private functions -----------------------------------------------------

    def Send_Base(self):
        x = 0                           + self.positionOffset[0]
        y = 0                           + self.positionOffset[1]
        z = self.baseRadius             + self.positionOffset[2]

        self.baseID = self.simulator.send_cylinder(x=x, y=y, z=z,
                                          r1=0, r2=1, r3=0,
                                          length = self.platformLength * 2, 
                                          radius = self.baseRadius,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=0.5, g=0.5, b=0.5,
                                          collision_group='env')

    def Send_Platform(self):
        x = 0                                         + self.positionOffset[0]
        y = 0                                         + self.positionOffset[1]
        z = self.baseRadius*2 + self.platformHeight/2 + self.positionOffset[2]

        self.platformID = self.simulator.send_box(x=x, y=y, z=z,
                                          length = self.platformLength,
                                          width  = self.platformWidth, 
                                          height = self.platformHeight,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env')

    def Send_Hinge(self):

        x = 0               + self.positionOffset[0]
        y = 0               + self.positionOffset[1]
        z = self.baseRadius + self.positionOffset[2]

        self.hingeID = self.simulator.send_hinge_joint(first_body_id  = self.baseID,
                                                       second_body_id = self.platformID,
                                                       x =x, y =y, z =z,
                                                       n1=0, n2=1, n3=0,
                                                       lo=-math.pi,
                                                       hi=+math.pi)
                                                       #speed=1.0, torque=10.0, position_control=True)
