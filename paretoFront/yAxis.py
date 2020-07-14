import localConstants as lc

from axis import AXIS

import pygame

class Y_AXIS(AXIS):

    def Set_Label(self):

        self.text = self.myfont.render(lc.yAxisLabel, True, lc.textColor)

        self.text = pygame.transform.rotate(self.text, 90)

    def Set_Label_Position(self):

        self.x = self.textrect.width/2

        self.y = lc.yAxisHeight/2

    def Set_Position(self):

        self.xStart = lc.yAxisIndentation
        self.xEnd   = self.xStart

        self.yStart = lc.depth - lc.xAxisIndentation
        self.yEnd   = 0

