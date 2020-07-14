import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

import constants as c

class CELL: 

    def __init__(self,i,j,top,left,bottom,right):

        self.rowIndex    = i
        self.columnIndex = j

        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

        self.center = (self.top + self.bottom) / 2

        self.centerBottom = 0.25 * self.top + 0.75 * self.bottom

        self.c = [1,1,1]

        self.str = ''

    def Draw(self,ax):

        self.Draw_Background(ax)

        self.Draw_Contents()

    def Draw_Text(self,txt):

        plt.text( x = self.left , y = self.center , s = txt )

    def Get_Bottom(self):

        return self.bottom

    def Get_Left(self):

        return self.left

    def Get_Right(self):

        return self.right

    def Get_Top(self):

        return self.top

    def Print(self):

        print( self.top , self.left , self.bottom , self.right )

    def Set_Color(self,c):

        self.c = c 

    def Set_Contents(self,str):

        self.str = str

# -------------------- Private methods ----------------------

    def Draw_Background(self,ax):

        leftTopVertex = [ self.left , self.top ]

        rightTopVertex = [ self.right , self.top ]

        rightBottomVertex = [ self.right , self.bottom ]

        leftBottomVertex = [ self.left , self.bottom ]

        polygonVertices = [ leftTopVertex , rightTopVertex , rightBottomVertex , leftBottomVertex ]

        rect = patches.Polygon( polygonVertices , closed = True , color = self.c )

        ax.add_patch(rect)

    def Draw_Contents(self):

        if c.colorNamesNoParens[self.columnIndex] == 'red':

            textColor = 'white'

        elif c.colorNamesNoParens[self.columnIndex] == 'blue':

            textColor = 'white'

        elif c.colorNamesNoParens[self.columnIndex] == 'purple':

            textColor = 'white'

        else:
            textColor = 'black'

        plt.text( x = self.left , y = self.bottom , s = self.str , color = textColor )        
