class ENV_BALL:

    def __init__(self, simulator):
        self.simulator = simulator

    def Get_Robot_Offset(self):
        x = .5
        y = 0
        z = 0

        return x, y, z

    def Send_To_Simulator(self,positionOffset,drawOffset,fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        self.Send_Box(self.simulator, self.positionOffset, self.drawOffset, self.fadeStrategy)
        self.Send_Ball(self.simulator, self.positionOffset, self.drawOffset, self.fadeStrategy)

    # --------------- Private functions -----------------------------------------------------

    def Send_Ball(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = 0 + positionOffset[0]
        y = 3 - 0.5 / 2 - 0.01 + positionOffset[1]
        z = 1.5 * 0.5 + positionOffset[2]

        self.ID = simulator.send_cylinder(x=x, y=y, z=z,
                                          length=0, radius=0.5 / 2,
                                          draw_offset_x=drawOffset[0],
                                          draw_offset_y=drawOffset[1],
                                          draw_offset_z=drawOffset[2],
                                          fade_strategy=fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env')

    def Send_Box(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = 0 + positionOffset[0]
        y = 3 + positionOffset[1]
        z = 0.5 / 2 + positionOffset[2]

        self.ID = simulator.send_box(x=x, y=y, z=z,
                                     length=0.5, width=0.5, height=0.5,
                                     draw_offset_x=drawOffset[0],
                                     draw_offset_y=drawOffset[1],
                                     draw_offset_z=drawOffset[2],
                                     fade_strategy=fadeStrategy,
                                     r=1, g=0, b=0,
                                     collision_group='env')
