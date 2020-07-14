import matplotlib.pyplot as plt

from visualizations.cell import CELL

class MATRIX:

    def __init__(self,numRows,numColumns,cellWidth):

        self.numRows = numRows

        self.numColumns = numColumns

        self.cellWidth = cellWidth

        self.Initialize_Cells()

    def Bottom(self):

        return -self.numRows * self.cellWidth

    def Draw(self,ax,primaryBotIndex):

        for i in range(0,self.numRows):

            for j in range(0,self.numColumns):

                if ( j == primaryBotIndex ):

                    self.cells[i][j].Draw(ax)

    def Left(self):

        return 0

    def On_Row_Draw_Text(self,i,txt):

        self.cells[i][0].Draw_Text(txt)

    def Print(self):

        for i in range(0,self.numRows):

            for j in range(0,self.numColumns):

                self.cells[i][j].Print()

    def Right(self):

        return self.numColumns * self.cellWidth

    def Set_Cell_Color(self , i , j , c):

        self.cells[i][j].Set_Color(c)

    def Set_Cell_Contents(self , i , j , str):

        self.cells[i][j].Set_Contents(str)

    def Top(self):

        return 0

    def Underline_Rows(self):

        for i in range(0,self.numRows):

            self.Underline_Row(i)

# --------------- Private methods -----------------

    def Initialize_Cells(self):

        self.cells = {}

        for i in range(0,self.numRows):

            self.cells[i] = {}

            for j in range(0,self.numColumns):

                top    = -i   * self.cellWidth
                left   = j    * self.cellWidth
                bottom = top  - self.cellWidth
                right  = left + self.cellWidth

                self.cells[i][j] = CELL(i,j,top,left,bottom,right)

    def Underline_Row(self,i):

        height = self.cells[i][0].Get_Bottom()

        left = self.cells[i][0].Get_Left()

        right = self.cells[i][self.numColumns-1].Get_Right()

        plt.plot([left,right],[height,height],'k-')
