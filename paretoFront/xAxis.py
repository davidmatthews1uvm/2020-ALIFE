import localConstants as lc

from axis import AXIS

class X_AXIS(AXIS):

    def Set_Label(self):

        self.text = self.myfont.render(lc.xAxisLabel, True, lc.textColor)

    def Set_Label_Position(self):

        self.x = lc.yAxisIndentation + lc.xAxisWidth/2

        self.y = lc.depth - self.textrect.height/2

    def Set_Position(self):

        self.xStart = lc.yAxisIndentation
        self.xEnd   = lc.width

        self.yStart = lc.depth - lc.xAxisIndentation
        self.yEnd   = self.yStart

