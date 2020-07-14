import math, pygame, random

import constants as c
import localConstants as lc

class ROBOT:

    def __init__(self,database,colorLetter,screen,numUndigestedReinforcements):

        self.screen      = screen.Get_Screen()

        self.numUndigestedReinforcements = numUndigestedReinforcements

        self.color       = c.colorLetterToPygameColor[colorLetter]

        colorIndex       = c.colorLetterToColorIndex[colorLetter]

        robotRecord      = database.Get_Youngest_Bot_Of_ColorIndex(colorIndex)

        robotID          = database.From_Robot_Record_Get_ID(robotRecord)

        self.wins        = database.Get_Robot_Num_Digested_Yeses(robotID)

        self.losses      = database.Get_Robot_Num_Digested_Nos(robotID)

        self.font        = pygame.font.Font("anonymous-pro.bold.ttf",lc.fontSize)
        self.fontText    = self.font.render(colorLetter, True, (0,0,0))

        self.xOffset     = lc.colorCharToCircleOffset[colorLetter][0]

        self.yOffset     = lc.colorCharToCircleOffset[colorLetter][1]

    def Add_Loss(self):

        self.losses = self.losses + 1

    def Add_Win(self):

        self.wins = self.wins + 1

    def Draw_Circle(self):

        pygame.draw.circle(self.screen,self.color,(self.x,self.y),lc.circleSize)

        self.Draw_Character(self.screen)

    def Draw_Losses(self,finishedPushingRobot):

        self.Draw_Losses_Line()

        self.Draw_Losses_Text(finishedPushingRobot)

    def Draw_Shadow(self):

        left = self.x
        top = self.y

        width  = lc.width - left
        height = (lc.depth - lc.xAxisIndentation) - top 

        area = (left,top,width,height)

        pygame.draw.rect(self.screen,(100,100,100),area)

    def Draw_Wins(self,finishedPushingRobot):

        self.Draw_Wins_Line()

        self.Draw_Wins_Text(finishedPushingRobot)

    def Get_Horizontal_Position(self):

        return self.x

    def Get_Pushed_Rightward(self):

        self.x = self.x + lc.speedOfReinforcement * self.numUndigestedReinforcements

        if self.x > self.Get_New_Target_X():

            self.x = self.Get_New_Target_X()

    def Get_Pushed_Upward(self):

        self.y = self.y - lc.speedOfReinforcement * self.numUndigestedReinforcements

        if self.y < self.Get_New_Target_Y():

            self.y = self.Get_New_Target_Y()

    def Get_Vertical_Position(self):

        return self.y

    def Not_At_Target_X_Yet(self):

        return self.Get_Horizontal_Position() < self.Get_New_Target_X()

    def Not_At_Target_Y_Yet(self):

        return self.Get_Vertical_Position() > self.Get_New_Target_Y()

    def Print(self):

        print(self.color)

    def Set_Max_Losses(self,maxLosses):

        self.maxLosses = maxLosses

    def Set_Max_Wins(self,maxWins):

        self.maxWins = maxWins

    def Set_Position(self):

        self.x = self.Convert_Losses_To_X_Position() + int(math.log(self.xOffset+1))

        self.y = self.Convert_Wins_To_Y_Position()   + int(math.log(self.yOffset+1))

# ----------------------- Private methods ------------------

    def Convert_Losses_To_X_Position(self):

        zeroToOne = math.log(self.losses+1) / math.log(self.maxLosses+1)

        zeroToXAxisWidth = zeroToOne * ( (1 - lc.leaveSpaceOnTheRight) * lc.xAxisWidth)

        # Ensures robot with max losses does not go beyond the right-hand edge of the window.

        yAxisIndentationToWidth = lc.yAxisIndentation + zeroToXAxisWidth

        return int(yAxisIndentationToWidth)

    def Convert_Wins_To_Y_Position(self):

        zeroToOne = math.log(self.wins+1) / math.log(self.maxWins+1)

        zeroToYAxisHeight = zeroToOne * ( (1 - lc.leaveSpaceAtTheTop) * lc.yAxisHeight)

        # Ensures robot with max wins does not go beyond the top edge of the window.

        y = lc.depth - lc.xAxisIndentation - zeroToYAxisHeight
        
        return int(y)

    def Draw_Character(self,screen):

        textrect = self.fontText.get_rect()
        textrect.centerx = self.x
        textrect.centery = self.y
        screen.blit(self.fontText, textrect )

    def Draw_Losses_Line(self):

        xStart = self.x 
        xEnd   = self.x

        yStart = self.y + lc.circleSize
        yEnd   = lc.depth - lc.yAxisIndentation

        start_pos = [xStart, yStart]
        end_pos   = [xEnd  , yEnd]

        pygame.draw.line(self.screen , self.color , start_pos , end_pos , lc.arrowLineWidth )

    def Draw_Losses_Text(self,finishedPushingRobot):

        if finishedPushingRobot:

            self.lossesText = self.font.render(str(self.losses+1), True, self.color)
        else:
            self.lossesText = self.font.render(str(self.losses), True, self.color)

        textrect = self.lossesText.get_rect()
        textrect.centerx = self.x
        textrect.centery = (lc.depth - lc.xAxisIndentation) + textrect.height/2 + lc.circleSize
        self.screen.blit(self.lossesText, textrect )

    def Draw_Wins_Line(self):

        xStart = lc.yAxisIndentation
        xEnd   = self.x - lc.circleSize

        yStart = self.y
        yEnd   = self.y

        start_pos = [xStart, yStart]
        end_pos   = [xEnd  , yEnd]

        pygame.draw.line(self.screen , self.color , start_pos , end_pos , lc.arrowLineWidth )

    def Draw_Wins_Text(self,finishedPushingRobot):

        if finishedPushingRobot:

            self.winsText = self.font.render(str(self.wins+1), True, self.color)
        else:
            self.winsText = self.font.render(str(self.wins), True, self.color)

        self.winsText = pygame.transform.rotate(self.winsText, 90)

        textrect = self.winsText.get_rect()
        textrect.centerx = lc.xAxisIndentation - textrect.width/2 - lc.circleSize
        textrect.centery = self.y
        self.screen.blit(self.winsText, textrect )

    def Get_Losses(self):

        return self.losses

    def Get_New_Target_Y(self):

        self.wins = self.wins + 1

        newTargetY = self.Convert_Wins_To_Y_Position()

        self.wins = self.wins - 1

        return newTargetY

    def Get_New_Target_X(self):

        self.losses = self.losses + 1

        newTargetX = self.Convert_Losses_To_X_Position()

        self.losses = self.losses - 1

        return newTargetX

    def Get_Wins(self):

        return self.wins
