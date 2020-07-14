import constantsPassiveGame as cpg

import constants as c

import time, datetime, os, pickle

class ACTIVE_USER:

    def __init__(self , userID , username , points , ptsPerSec ):

        self.userID = userID

        self.username = username

        self.initialPoints = points

        filename = "../data/" + self.username + "Pts.p"

        self.ptsPerSec = ptsPerSec

        self.datetimeOfMostRecentChat = self.Ages_Ago()

    def Draw_To(self,screen,row):

        self.Compute_Text_Color()

        self.Draw_Points_To(screen,row)

        self.Draw_PtsPerSec_To(screen,row)

        self.Draw_Name_To(screen,row)

    def Get_Points(self):

        return self.points

    def Get_Pts_Per_Sec(self):

        return self.ptsPerSec

    def Print(self):

        print( self.username )

        print( self.points )

        print( self.ptsPerSec )

    def Update_Datetime_Of_Most_Recent_Chat(self,datetimeOfRecentChat):

        if datetimeOfRecentChat > self.datetimeOfMostRecentChat:

            self.datetimeOfMostRecentChat = datetimeOfRecentChat

    def Update_Points(self):

        self.points = self.initialPoints + self.ptsPerSec * self.Seconds_Since_Last_Chat()

# -------------- Private methods -------------------

    def Ages_Ago(self):

        return datetime.datetime.fromtimestamp( time.time() - 1000000 )

    def Chatbot_Needs_Points(self):

        filename = "../data/needPtsFor"+self.username+".dat"

        return os.path.isfile(filename)

    def Compute_Text_Color(self):

        datetimeSinceMostRecentChat = datetime.datetime.now() - self.datetimeOfMostRecentChat

        secondsSinceMostRecentChat = datetimeSinceMostRecentChat.total_seconds()

        zeroToOne = secondsSinceMostRecentChat / cpg.inactivateUserAfter

        zeroTo255 = int(zeroToOne * 255)

        fadeFromBlackToWhite = 255 - zeroTo255

        if fadeFromBlackToWhite < 0:

            fadeFromBlackToWhite = 0

        self.textColor = ( fadeFromBlackToWhite , fadeFromBlackToWhite , fadeFromBlackToWhite )

    def Draw_Name_To(self,screen,row):

        panel = screen.Get_Panel( row , cpg.columnForUserNames )

        panel.Draw_Text( screen.Get_Screen() , self.username , justification = 'left' , color = self.textColor)

    def Draw_Points_To(self,screen,row):

        panel = screen.Get_Panel( row , cpg.columnForPoints )

        textScore = '%.2f' % self.points 

        panel.Draw_Text( screen.Get_Screen() , textScore , justification = 'right' , color = self.textColor)

    def Draw_PtsPerSec_To(self,screen,row):

        panel = screen.Get_Panel( row , cpg.columnForPtsPerSec )

        panel.Draw_Text( screen.Get_Screen() , str(self.ptsPerSec) , justification = 'center' , color = self.textColor)

    def Seconds_Since_Last_Chat(self):

        datetimeSinceMostRecentChat = datetime.datetime.now() - self.datetimeOfMostRecentChat

        return datetimeSinceMostRecentChat.total_seconds()
