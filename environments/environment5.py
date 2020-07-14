import math

class ENVIRONMENT5:

    def __init__(self, simulator):
        self.simulator = simulator

        self.standHeight = 0.25 
        self.standWidth  = self.standHeight
        self.standLength = self.standHeight

        self.beamHeight  = self.standHeight / 4
        self.beamWidth   = 8 * self.standWidth 
        self.beamLength  = self.beamHeight

    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = 0

        return x, y, z

    def Send_To_Simulator(self,positionOffset, drawOffset, fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        self.Send_Left_Red_Stand()

        self.Send_Right_Blue_Stand()

        self.Send_Green_Beam()

    # --------------- Private functions -----------------------------------------------------

    def Send_Left_Red_Stand(self):
        x = -3 * self.standWidth  + self.positionOffset[0]
        y = +2 * self.standLength + self.positionOffset[1]
        z = self.standHeight / 2  + self.positionOffset[2]

        self.leftStandID = self.simulator.send_box(x=x, y=y, z=z,
                                          length = self.standLength,
                                          width  = self.standWidth, 
                                          height = self.standHeight,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env')

    def Send_Green_Beam(self):
        x = 0                                    + self.positionOffset[0]
        y = +2 * self.standLength                + self.positionOffset[1]
        z = self.standHeight + self.beamHeight/2 + self.positionOffset[2]

        self.beamID = self.simulator.send_box(x=x, y=y, z=z,
                                          length = self.beamLength,
                                          width  = self.beamWidth,
                                          height = self.beamHeight,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=0, g=1, b=0,
                                          collision_group='env')

    def Send_Right_Blue_Stand(self):
        x = +3 * self.standWidth  + self.positionOffset[0]
        y = +2 * self.standLength + self.positionOffset[1]
        z = self.standHeight / 2  + self.positionOffset[2]

        self.rightStandID = self.simulator.send_box(x=x, y=y, z=z,
                                          length = self.standLength,
                                          width  = self.standWidth,
                                          height = self.standHeight,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=0, g=0, b=1,
                                          collision_group='env')
