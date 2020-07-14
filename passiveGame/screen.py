import constantsPassiveGame as cpg

import pygame

from passiveGame.panels import PANELS

class SCREEN:

    def __init__(self):

        pygame.init()

        actualDepth = cpg.depth + cpg.panelDepth # Add a row at the bottom for the ticker tape

        self.screen = pygame.display.set_mode((cpg.width,actualDepth)) # Set screen size of pygame window

        pygame.font.init()

        self.myfont = pygame.font.Font(cpg.font,cpg.fontSize)

        self.panels = PANELS(self.myfont)

        self.done = False

    def Done(self):

        return self.done

    def Get_Panel(self,column,row):

        return self.panels.Get_Panel(column,row)

    def Get_Screen(self):

        return self.screen

    def Handle_Events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                # self.done = True
                exit()

    def Prepare(self):

        self.screen.fill(cpg.backgroundColor)

        self.Draw_Lines()

        self.Draw_Titles()

        #self.panels.Draw(self.screen)

    def Reveal(self):

        pygame.display.flip()

# ----------- Private meethods ------------

    def Draw_Lines(self):

        self.Draw_Horizontal_Lines()

        self.Draw_Vertical_Lines()

    def Draw_Titles(self):

        for column in range(0,cpg.numColumns):

            panel = self.panels.Get_Panel( cpg.rowForTitles , column )

            panel.Draw_Text(self.screen, cpg.titles[column] , justification = cpg.columnJustifications[column] , color = (255,255,255) )

    def Draw_Horizontal_Lines(self):

        for row in range(1,cpg.numRows+1):

            y = row * cpg.columnHeight

            leftX = 0

            rightX = cpg.width

            color = [100,100,100]

            start_pos = [ leftX , y ]

            end_pos = [ rightX , y ]

            if row == 1 or row == cpg.numRows:

                lineWidth = 5
            else:
                lineWidth = 1

            pygame.draw.line(self.screen , color , start_pos , end_pos , lineWidth )

    def Draw_Vertical_Lines(self):

        x = 0

        for column in range(1,cpg.numColumns):

            x = x + cpg.width * cpg.columnWidths[column-1]

            topY = 0

            bottomY = cpg.depth

            color = [100,100,100]

            start_pos = [ x , topY ]

            end_pos = [ x , bottomY ]

            if column == 3:
                lineWidth = 5
            else:
                lineWidth = 1

            pygame.draw.line(self.screen , color , start_pos , end_pos , lineWidth ) 

