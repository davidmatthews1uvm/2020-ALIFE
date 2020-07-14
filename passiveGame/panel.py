import constantsPassiveGame as cpg

import pygame

import random

import time

class PANEL:

    def __init__(self,row,column,myfont):

        self.row = row

        self.column = column

        self.myfont = myfont

        self.y = row * cpg.panelDepth

        self.x = 0

        for col in range(0,self.column):

            self.x = self.x + cpg.width * cpg.columnWidths[col] 

        self.panelWidth = cpg.width * cpg.columnWidths[self.column]

        self.creationTime = time.time()

    def Draw_Text(self,screen,textString, justification = 'left', color = (0,0,0)):

        self.Draw_To_Panel(screen,textString,justification,color)

# -------------- Private methods --------------------------

    def Draw_To_Panel(self,screen,textString, justification = 'left', color = (0,0,0)):

        textsurface = self.myfont.render(textString, True, color)

        textrect = textsurface.get_rect()

        if ( justification == 'left' ):

            textrect.centerx = self.x + textrect.width/2 + cpg.textPadding

        elif ( justification == 'center' ):

            textrect.centerx = self.x + (self.panelWidth-textrect.width)/2 + textrect.width/2

        else: # right justified

            textrect.centerx = self.x + self.panelWidth - textrect.width/2 - cpg.textPadding
 
        textrect.centery = self.y + (cpg.panelDepth-textrect.height)/2 + textrect.height/2

        screen.blit( textsurface , textrect )
