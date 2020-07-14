import pygame

from reinforcement import REINFORCEMENT 

import sys
sys.path.append('..')

import localConstants as lc

class WIN(REINFORCEMENT):

    def Add_To_Robot(self):

        self.robot.Add_Win()

    def Done(self):

        return self.y < -self.height/2

    def Draw_Robots_Wins_Or_Losses(self):

        self.robot.Draw_Wins(self.Finished_Pushing_Robot())

    def Finished_Pushing_Robot(self):

        heightOfTopmostEdge = self.textrect.centery - self.textrect.height/2

        centerOfCircle = self.robot.Get_Vertical_Position()

        return heightOfTopmostEdge < centerOfCircle 

    def Robot_Can_Be_Pushed_Upward(self):

        return self.Touching_Bottom_Of_Robot() and self.robot.Not_At_Target_Y_Yet()

    def Rotate_Text(self):

        self.text = pygame.transform.rotate(self.text, 90)

    def Set_Position(self):

        self.x = self.robot.Get_Horizontal_Position()

        self.y = lc.depth + self.textrect.height/2

    def Update(self):

        self.y = self.y - lc.speedOfReinforcement * self.numUndigestedReinforcements

        if self.Robot_Can_Be_Pushed_Upward():

            self.robot.Get_Pushed_Upward()

    def Robot_Can_Be_Pushed_Upward(self):

        touchingBottomOfRobot = self.Touching_Bottom_Of_Robot()

        notAtTargetYYet = self.robot.Not_At_Target_Y_Yet()

        return self.Touching_Bottom_Of_Robot() and self.robot.Not_At_Target_Y_Yet()

    def Touching_Bottom_Of_Robot(self):

        heightOfTopmostEdge = self.textrect.centery - self.textrect.height/2

        lowerEdgeOfCircle = self.robot.Get_Vertical_Position() + lc.circleSize

        return heightOfTopmostEdge < lowerEdgeOfCircle 
