class ENV_SEESAW:

    def __init__(self, simulator):
        self.simulator = simulator

    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = .8

        return x, y, z

    def Send_To_Simulator(self,positionOffset,drawOffset,fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        cyl = self.Send_Cylinder(self.simulator, [0, 0, .3], self.drawOffset, self.fadeStrategy)
        ramp = self.Send_Ramp(self.simulator, [0, 0, .3], self.drawOffset, self.fadeStrategy)

        slider_joint = self.simulator.send_slider_joint(first_body_id=cyl,
                                                        second_body_id=ramp,
                                                        x=0, y=0, z=0.0,
                                                        lo=-0, hi=0)

    # --------------- Private functions -----------------------------------------------------

    def Send_Cylinder(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = 0 + positionOffset[0]
        y = positionOffset[1]
        z = positionOffset[2]

        self.ID = simulator.send_cylinder(x=x, y=y, z=z,
                                          length=0.5, radius=0.3,
                                          r1=0, r2=1, r3=0,
                                          draw_offset_x=drawOffset[0],
                                          draw_offset_y=drawOffset[1],
                                          draw_offset_z=drawOffset[2],
                                          fade_strategy=fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env',
                                          mass=10)

        return self.ID

    def Send_Ramp(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = positionOffset[0]
        y = positionOffset[1]
        z = .15 + positionOffset[2]

        self.ID = simulator.send_box(x=x, y=y, z=z,
                                     length=0.8, width=3, height=0.1,
                                     draw_offset_x=drawOffset[0],
                                     draw_offset_y=drawOffset[1],
                                     draw_offset_z=drawOffset[2],
                                     fade_strategy=fadeStrategy,
                                     r=1, g=0, b=0,
                                     collision_group='env',
                                     mass=10)

        return self.ID
