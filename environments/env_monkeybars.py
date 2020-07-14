class ENV_MONKEYBARS:

    def __init__(self, simulator):
        self.simulator = simulator

    def Get_Robot_Offset(self):
        x = 0
        y = 0
        z = 1.5

        return x, y, z

    def Send_To_Simulator(self,positionOffset, drawOffset, fadeStrategy):
        self.positionOffset = positionOffset
        self.drawOffset = drawOffset
        self.fadeStrategy = fadeStrategy

        self.support1 = self.Send_Box(self.simulator, [-0.5, 0, 0.35], self.drawOffset, self.fadeStrategy, 0.6)
        self.support2 = self.Send_Box(self.simulator, [1.5, 0, 0.35], self.drawOffset, self.fadeStrategy, 0.6)
        self.support3 = self.Send_Support(self.simulator, [0.5, -.4, 0.55], self.drawOffset, self.fadeStrategy)
        self.support4 = self.Send_Support(self.simulator, [0.5, .4, 0.55], self.drawOffset, self.fadeStrategy)

        joint1 = self.simulator.send_hinge_joint(first_body_id=self.support1, second_body_id=self.support3, x=0, y=0.0,
                                                 z=0, lo=0, hi=0)
        joint2 = self.simulator.send_hinge_joint(first_body_id=self.support1, second_body_id=self.support4, x=0, y=0.0,
                                                 z=0, lo=0, hi=0)
        joint3 = self.simulator.send_hinge_joint(first_body_id=self.support2, second_body_id=self.support3, x=0, y=0.0,
                                                 z=0, lo=0, hi=0)
        joint4 = self.simulator.send_hinge_joint(first_body_id=self.support2, second_body_id=self.support4, x=0, y=0.0,
                                                 z=0, lo=0, hi=0)

        self.bar1 = self.Send_Cylinder(self.simulator, [0, 0, 0.55], self.drawOffset, self.fadeStrategy)
        self.bar2 = self.Send_Cylinder(self.simulator, [.5, 0, 0.55], self.drawOffset, self.fadeStrategy)
        self.bar3 = self.Send_Cylinder(self.simulator, [1, 0, 0.55], self.drawOffset, self.fadeStrategy)

        bar_joint1 = self.simulator.send_hinge_joint(first_body_id=self.bar1, second_body_id=self.support3, x=0, y=0.0,
                                                     z=0, lo=0, hi=0)
        bar_joint2 = self.simulator.send_hinge_joint(first_body_id=self.bar1, second_body_id=self.support4, x=0, y=0.0,
                                                     z=0, lo=0, hi=0)
        bar_joint3 = self.simulator.send_hinge_joint(first_body_id=self.bar2, second_body_id=self.support3, x=0, y=0.0,
                                                     z=0, lo=0, hi=0)
        bar_joint4 = self.simulator.send_hinge_joint(first_body_id=self.bar2, second_body_id=self.support4, x=0, y=0.0,
                                                     z=0, lo=0, hi=0)
        bar_joint5 = self.simulator.send_hinge_joint(first_body_id=self.bar3, second_body_id=self.support3, x=0, y=0.0,
                                                     z=0, lo=0, hi=0)
        bar_joint6 = self.simulator.send_hinge_joint(first_body_id=self.bar3, second_body_id=self.support4, x=0, y=0.0,
                                                     z=0, lo=0, hi=0)

        # --------------- Private functions -----------------------------------------------------

    def Send_Cylinder(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = positionOffset[0]
        y = positionOffset[1]
        z = positionOffset[2]

        self.ID = simulator.send_cylinder(x=x - .25, y=y, z=z,
                                          length=.8, radius=.1,
                                          r1=0, r2=1, r3=0,
                                          draw_offset_x=drawOffset[0],
                                          draw_offset_y=drawOffset[1],
                                          draw_offset_z=drawOffset[2],
                                          fade_strategy=fadeStrategy,
                                          r=1, g=0, b=0,
                                          collision_group='env')

        return self.ID

    def Send_Box(self, simulator, positionOffset, drawOffset, fadeStrategy, height):
        x = positionOffset[0]
        y = positionOffset[1]
        z = positionOffset[2]

        return simulator.send_box(x=x - .25, y=y, z=z,
                                  length=1, width=0.25, height=height,
                                  draw_offset_x=drawOffset[0],
                                  draw_offset_y=drawOffset[1],
                                  draw_offset_z=drawOffset[2],
                                  fade_strategy=fadeStrategy,
                                  r=1, g=0, b=0,
                                  collision_group='env',
                                  mass=10)

    def Send_Support(self, simulator, positionOffset, drawOffset, fadeStrategy):
        x = positionOffset[0]
        y = positionOffset[1]
        z = positionOffset[2]

        return simulator.send_box(x=x - .25, y=y, z=z,
                                  length=.2, width=2.25, height=.2,
                                  draw_offset_x=drawOffset[0],
                                  draw_offset_y=drawOffset[1],
                                  draw_offset_z=drawOffset[2],
                                  fade_strategy=fadeStrategy,
                                  r=1, g=0, b=0,
                                  collision_group='env',
                                  mass=10)
