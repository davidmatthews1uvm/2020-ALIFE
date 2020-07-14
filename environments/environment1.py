class ENVIRONMENT1:

    def __init__(self, simulator):
        self.simulator = simulator

    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = 0

        return x, y, z

    def Send_To_Simulator(self,positionOffset, drawOffset, fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        self.Send_Box()

    # --------------- Private functions -----------------------------------------------------

    def Send_Box(self):
        x = 0 + self.positionOffset[0]
        y = 8 + self.positionOffset[1]
        z = 0.5 / 2 + self.positionOffset[2]

        self.ID = self.simulator.send_box(x=x, y=y, z=z,
                                          length=0.5, width=0.5, height=0.5,
                                          draw_offset_x=self.drawOffset[0],
                                          draw_offset_y=self.drawOffset[1],
                                          draw_offset_z=self.drawOffset[2],
                                          fade_strategy=self.fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env')
