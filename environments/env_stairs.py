class ENV_STAIRS:

    def __init__(self, simulator):
        self.simulator = simulator

    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = .6

        return x, y, z

    def Send_To_Simulator(self,positionOffset, drawOffset, fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        self.stair1 = self.Send_Box(self.simulator, [-0.35, 0, 0.10], self.drawOffset, self.fadeStrategy, 0.05)
        self.stair2 = self.Send_Box(self.simulator, [-0.1, 0, 0.15], self.drawOffset, self.fadeStrategy, .15)
        self.stair3 = self.Send_Box(self.simulator, [0.15, 0, 0.2], self.drawOffset, self.fadeStrategy, .25)
        self.stair4 = self.Send_Box(self.simulator, [0.4, 0, 0.25], self.drawOffset, self.fadeStrategy, .35)

        joint = self.simulator.send_hinge_joint(first_body_id=self.stair1, second_body_id=self.stair2, x=0, y=0.0, z=0,
                                                lo=0, hi=0)
        joint2 = self.simulator.send_hinge_joint(first_body_id=self.stair2, second_body_id=self.stair3, x=0, y=0.0, z=0,
                                                 lo=0, hi=0)
        joint3 = self.simulator.send_hinge_joint(first_body_id=self.stair3, second_body_id=self.stair4, x=0, y=0.0, z=0,
                                                 lo=0, hi=0)

        # --------------- Private functions -----------------------------------------------------

    def Send_Box(self, simulator, positionOffset, drawOffset, fadeStrategy, height):
        x = positionOffset[0]
        y = positionOffset[1]
        z = positionOffset[2]

        return simulator.send_box(x=x - .25, y=y + .25, z=z,
                                  length=1, width=0.25, height=height,
                                  draw_offset_x=drawOffset[0],
                                  draw_offset_y=drawOffset[1],
                                  draw_offset_z=drawOffset[2],
                                  fade_strategy=fadeStrategy,
                                  r=1, g=0, b=0,
                                  collision_group='env',
                                  mass=10)
