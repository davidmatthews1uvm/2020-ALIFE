import constants as c

import localConstants as lc

import numpy as np

import math

import pygame

from axes import AXES

class SCREEN:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((lc.width,lc.depth))

        pygame.font.init()

        self.myfont = pygame.font.Font("anonymous-pro.bold.ttf",lc.fontSize)

        self.done = False

        self.axes = AXES(self.screen,self.myfont)

    def Add_Axes(self):

        self.axes.Draw()

    def Add_Title(self):

        titleText = self.myfont.render("?shadow", True, lc.textColor)

        textrect = titleText.get_rect()

        textrect.centerx = lc.yAxisIndentation + lc.xAxisWidth/2

        textrect.centery = textrect.height/2 

        self.screen.blit(titleText, textrect )
        
    def Done(self):

        return self.done

    def Draw_Sun(self,maxLosses,maxWins):

        yellowColor = c.colorLetterToPygameColor['y']

        pygame.draw.circle(self.screen,yellowColor,(0,0),lc.circleSize * lc.sizeOfSun)

        xStart = 0

        yStart = 0

        for theta in np.linspace( 0 ,2 * math.pi , lc.numberOfSunsRays ):

            r = lc.lengthOfSunsRays

            xEnd = r * math.sin(theta)

            yEnd = r * math.cos(theta)

            start_pos = [xStart, yStart]
            end_pos   = [xEnd  , yEnd]

            pygame.draw.line(self.screen , yellowColor , start_pos , end_pos , lc.arrowLineWidth )
            
 
    def Get_MyFont(self):

        return self.myfont

    def Get_Screen(self):

        return self.screen
 
    def Prepare(self):

        self.screen.fill((0,0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.done = True

    def Reveal(self):

        pygame.display.update()
