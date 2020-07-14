import pygame

from xAxis import X_AXIS

from yAxis import Y_AXIS

class AXES:

    def __init__(self,screen,myfont):

        self.xAxis = X_AXIS(screen,myfont)

        self.yAxis = Y_AXIS(screen,myfont)

    def Draw(self):

        self.xAxis.Draw()

        self.yAxis.Draw()
