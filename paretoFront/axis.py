import localConstants as lc

import math, pygame

import numpy as np

from abc import ABC, abstractmethod

class AXIS(ABC):

    def __init__(self,screen,myfont):

        super().__init__()

        self.screen = screen

        self.myfont = myfont

        self.Set_Label()

        self.textrect = self.text.get_rect()

        self.Set_Label_Position()

        self.textrect.centerx = self.x

        self.textrect.centery = self.y

    def Draw(self):

        self.Set_Position()

        self.Draw_Arrow(     self.xStart,self.xEnd,self.yStart,self.yEnd)

        self.Draw_Arrow_Head(self.xStart,self.xEnd,self.yStart,self.yEnd,direction='left')

        self.Draw_Arrow_Head(self.xStart,self.xEnd,self.yStart,self.yEnd,direction='right')

        self.Add_Label()

# -------------------------- Private methods ------------------------

    def Add_Label(self):

        self.screen.blit(self.text, self.textrect )

    def Cartesian_To_Polar_Coordinates(self, x, y):

        rho = np.sqrt(x**2 + y**2)

        phi = np.arctan2(y, x)

        return(rho, phi)

    def Draw_Arrow(self,xStart,xEnd,yStart,yEnd):

        start_pos = [xStart, yStart]
        end_pos   = [xEnd  , yEnd]

        color = (255,255,255)

        pygame.draw.line(self.screen , color , start_pos , end_pos , lc.arrowLineWidth )

    def Draw_Arrow_Head(self,xStart,xEnd,yStart,yEnd,direction):

        x = xEnd - xStart

        y = yEnd - yStart

        rho, phi = self.Cartesian_To_Polar_Coordinates(x,y)

        newRho = rho * lc.arrowHeadSize

        if direction == 'left':

            newPhi = phi - math.pi/2 - math.pi / 4
        else:
            newPhi = phi + math.pi/2 + math.pi / 4

        x,y = self.Polar_To_Cartesian_Coordinates(newRho,newPhi)

        xStart = xEnd
        xEnd   = xEnd + x

        yStart = yEnd
        yEnd   = yEnd + y

        self.Draw_Arrow(xStart,xEnd,yStart,yEnd)

    def Polar_To_Cartesian_Coordinates(self, rho, phi):

        x = rho * np.cos(phi)

        y = rho * np.sin(phi)

        return(x, y)

    @abstractmethod
    def Set_Label(self):

        raise NotImplementedError()

    @abstractmethod
    def Set_Label_Position(self):

        raise NotImplementedError()

    @abstractmethod
    def Set_Position(self):

        raise NotImplementedError()

