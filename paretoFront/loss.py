from reinforcement import REINFORCEMENT 

import sys
sys.path.append('..')

import localConstants as lc

class LOSS(REINFORCEMENT):

    def Add_To_Robot(self):

        self.robot.Add_Loss()

    def Done(self):

        return self.x > lc.width + self.width/2

    def Draw_Robots_Wins_Or_Losses(self):

        self.robot.Draw_Losses(self.Finished_Pushing_Robot())

    def Finished_Pushing_Robot(self):

        xOfRightmostEdge = self.textrect.centerx + self.textrect.width/2

        xOfCirclesCenter = self.robot.Get_Horizontal_Position()

        return xOfRightmostEdge >= xOfCirclesCenter

    def Robot_Can_Be_Pushed_Rightward(self):

        return self.Touching_Left_Side_Of_Robot() and self.robot.Not_At_Target_X_Yet()

    def Rotate_Text(self):

        pass

    def Set_Position(self):

        self.x = -self.textrect.width/2

        self.y = self.robot.Get_Vertical_Position()

    def Update(self):

        self.x = self.x + lc.speedOfReinforcement * self.numUndigestedReinforcements

        if self.Robot_Can_Be_Pushed_Rightward():

            self.robot.Get_Pushed_Rightward()

    def Touching_Left_Side_Of_Robot(self):

        xOfRightmostEdge = self.textrect.centerx + self.textrect.width/2

        xOfCirclesLeftmostEdge = self.robot.Get_Horizontal_Position()  - lc.circleSize

        return xOfRightmostEdge >= xOfCirclesLeftmostEdge 
