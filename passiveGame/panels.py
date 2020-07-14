import constantsPassiveGame as cpg

from passiveGame.panel import PANEL

class PANELS:

    def __init__(self,myfont):

        self.panels = {}

        for row in range(0,cpg.numRows):

            for column in range(0,cpg.numColumns):

                self.panels[row,column] = PANEL(row,column,myfont) 

    def Draw(self,screen):

        for row in range(0,cpg.numRows):

            for column in range(0,cpg.numColumns-1):

                self.panels[row,column].Draw(screen)

    def Get_Panel(self,row,column):

        return self.panels[ row , column ]

    def Print(self):

        print(self.panels)
