import math,os

import constantsPassiveGame as cpg

class OPTION:

    def __init__(self,option):

        self.option      = option

        self.row         = 1 + self.option # Include the title row

        self.whatCanIDo  = cpg.options[option][0]

        self.cost        = cpg.options[option][1]

        self.whatDoIType = cpg.options[option][2]

        self.drawnLastTime = False

    def Do_Not_Draw(self):

        self.drawnLastTime = False

    def Draw_Gray_To(self,screen,maxPts,ptsPerSec):

        color = (125,125,125)

        # self.Draw_To(screen,color)

        self.Draw_Countdown(screen,color,maxPts,ptsPerSec)

        self.drawnLastTime = False

    def Draw_Question_Marks(self,screen):

        color = (125,125,125)

        self.Draw_Qs_In_WhatCanIDo_To(screen,color)

        self.Draw_Qs_In_Cost_To(screen,color)

        self.Draw_Qs_In_WhatDoIType_To(screen,color)

    def Draw_White_To(self,screen):

        color = (255,255,255)

        self.Draw_To(screen,color)

        if not self.drawnLastTime:

            os.system("afplay /System/Library/Sounds/Glass.aiff &")

        self.drawnLastTime = True

    def Get_Cost(self):

        return self.cost

    def Is_Affordable(self,highestScore):

        return self.Is_Too_Expensive(highestScore) == False

    def Is_Too_Expensive(self,highestScore):

        return self.cost > highestScore

    def Is_Unlock_Env_Option( self ):

        return self.option == cpg.unlockEnvRequest

    def Replace_Command_In_What_Can_I_Do_With( self , command ):

        leftOfExclamationPoint , exclamationPoint , rightOfExclamationPoint = self.whatCanIDo.partition('!')

        oldCommand , period , rightOfPeriod = rightOfExclamationPoint.partition('.')

        self.whatCanIDo = leftOfExclamationPoint + exclamationPoint + command + period + rightOfPeriod

    def Replace_Last_Word_In_What_Can_I_Do_With( self , newColor ):

        rest , space, lastWord = self.whatCanIDo.rpartition(' ')

        self.whatCanIDo = rest + ' ' + newColor 

    def Replace_Second_Word_In_What_Can_I_Do_With( self , newColor ):

        firstWord, space, rest = self.whatCanIDo.partition(' ')

        secondWord, space, rest = rest.partition(' ')

        self.whatCanIDo = firstWord + ' ' + newColor + ' ' + rest

    def Set_What_Do_I_Type_To(self,newString):

        self.whatDoIType = newString

# ------------ Private methods --------------

    def Draw_Cost_To(self,screen,color):

        column = cpg.columnForCost

        panel = screen.Get_Panel( self.row , column )

        panel.Draw_Text(screen.Get_Screen(), str( self.cost ) , cpg.columnJustifications[column] , color ) 

    def Draw_Countdown(self,screen,color,maxPts,ptsPerSec):

        self.Draw_Qs_In_WhatCanIDo_To(screen,color)

        self.Draw_Cost_To(screen,color)

        self.Draw_WhatDoIType_Countdown(screen,color,maxPts,ptsPerSec)

    def Draw_In_Color(self,color):

        if not color == (255,255,255):

            return False

        steal            = self.option == cpg.stealRequest

        buy              = self.option == cpg.buyRequest

        aggReinforcement = self.option == cpg.aggressorReinforcementRequest

        defReinforcement = self.option == cpg.defenderReinforcementRequest

        colorizedOption  = steal or buy or aggReinforcement or defReinforcement

        return colorizedOption

    def Draw_Qs_In_Cost_To(self,screen,color):

        column = cpg.columnForCost

        panel = screen.Get_Panel( self.row , column )

        panel.Draw_Text(screen.Get_Screen(), '???' , cpg.columnJustifications[column] , color )

    def Draw_Qs_In_WhatCanIDo_To(self,screen,color):

        column = cpg.columnForWhatCanIDo

        panel = screen.Get_Panel( self.row , column )

        panel.Draw_Text(screen.Get_Screen(), '???' , cpg.columnJustifications[column] , color )

    def Draw_Qs_In_WhatDoIType_To(self,screen,color):

        column = cpg.columnForWhatDoIType

        panel = screen.Get_Panel( self.row , column )

        panel.Draw_Text(screen.Get_Screen(), '???' , cpg.columnJustifications[column] , color )

    def Draw_To(self,screen,color):

        self.Draw_WhatCanIDo_To(screen,color)

        self.Draw_Cost_To(screen,color)

        self.Draw_WhatDoIType_To(screen,color)

    def Draw_WhatCanIDo_To(self,screen,color):

        column = cpg.columnForWhatCanIDo

        panel = screen.Get_Panel( self.row , column )

        panel.Draw_Text(screen.Get_Screen(), self.whatCanIDo , cpg.columnJustifications[column] , color )

    def Draw_WhatDoIType_Countdown(self,screen,color,maxPts,ptsPerSec):

        column = cpg.columnForWhatDoIType

        panel = screen.Get_Panel( self.row , column )

        if self.Draw_In_Color(color):

            color = self.Set_Color()

        pointsRequired = self.cost - maxPts

        minutesRemaining = 0

        secondsRemaining = pointsRequired / ptsPerSec # In seconds

        if secondsRemaining > 60.0:

            minutesRemaining = math.floor(secondsRemaining / 60)

            secondsRemaining = secondsRemaining - minutesRemaining * 60

        textRemaining = '%dm%ds' % (minutesRemaining,secondsRemaining)

        msg = "Next level unlocked in " + textRemaining

        panel.Draw_Text(screen.Get_Screen(), msg , cpg.columnJustifications[column] , color )

    def Draw_WhatDoIType_To(self,screen,color):

        column = cpg.columnForWhatDoIType

        panel = screen.Get_Panel( self.row , column )

        if self.Draw_In_Color(color):

            color = self.Set_Color()

        panel.Draw_Text(screen.Get_Screen(), self.whatDoIType , cpg.columnJustifications[column] , color )

    def Set_Color(self):

        if self.option==cpg.aggressorReinforcementRequest:

            colorChar = self.whatDoIType[0]

        elif self.option == cpg.defenderReinforcementRequest:

            colorChar = self.whatDoIType[0]
        else:
            colorChar = self.whatDoIType[1]

        return cpg.colorCharToPygameColor[colorChar]
