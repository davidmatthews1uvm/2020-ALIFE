import sys
sys.path.append('..')

import datetime, math, os

from database.database import DATABASE

import matplotlib.pyplot as plt

class HIGH_SCORES:

    def __init__(self,database):

        self.database = database

        self.leftEdge = 1000

        self.rightEdge = -1000

        self.topEdge = -1000

        self.bottomEdge = +1000

        self.farLeftMargin = 0.0

        self.leftMargin = 0.35

        self.centerMargin = 0.5

        self.rightMargin = 0.65

        self.topRow = 0.9

        self.rowHeight = 0.095

        self.Get_All_Users()

        self.Get_High_Scorers()

        self.Make_Ago_String()

        self.Find_Pareto_Front()

        self.Delete_Dominated_Users()

    def Clean_Up(self):

        self.ax.set_xticks([])

        self.ax.set_yticks([])

    def Delete_Dominated_Users(self):

        for user in list( self.highScorers.keys() ):

            if self.highScorers[user][3]:

                del self.highScorers[user]

    def Draw(self):

        plt.rcParams.update({
            "lines.color": "white",
            "patch.edgecolor": "white",
            "text.color": "white",
            "axes.facecolor": "black",
            "axes.edgecolor": "black",
            "axes.labelcolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "lightgray",
            "figure.facecolor": "black",
            "figure.edgecolor": "black",
            "savefig.facecolor": "black",
            "savefig.edgecolor": "black"})

        plt.rcParams.update({'font.size': 18})

        self.fig, self.ax = plt.subplots(1)

        self.Draw_Title()

        self.Draw_High_Scorers()

        self.Clean_Up()

        # plt.show()

    def Draw_High_Scorers(self):

        userRank = 0

        for username in self.highScorers: 

            pts = math.floor(self.highScorers[username][1])

            ago = self.highScorers[username][4]

            textHeight = self.topRow - (0 + userRank) * self.rowHeight

            plt.text( x = self.leftMargin  , y = textHeight , s = username, horizontalalignment = 'right'  )

            plt.text( x = self.centerMargin, y = textHeight , s = pts     , horizontalalignment = 'center' )

            plt.text( x = self.rightMargin , y = textHeight , s = ago     , horizontalalignment = 'left' )

            userRank = userRank + 1

    def Draw_Title(self):

            textHeight = self.topRow + 1.5 * self.rowHeight

            plt.text( x = self.leftMargin,   y = textHeight , s = 'Top players'   , horizontalalignment = 'right' )

            plt.text( x = self.centerMargin, y = textHeight , s = 'XP'      , horizontalalignment = 'center' )

            plt.text( x = self.rightMargin , y = textHeight , s = 'Joined'  , horizontalalignment = 'left' )

    def Find_Pareto_Front(self):

        self.Make_Everyone_Non_Dominated()

        self.Tag_Dominated_Users()

    def Get_All_Users(self):

       self.allUsers = database.Get_Users()

    def Get_High_Scorers(self):

        self.highScorers = {}

        for user in self.allUsers:

            userID = self.database.From_User_Record_Get_Id(user)

            userName = self.database.From_User_Record_Get_Name(user)

            userDate = self.database.From_User_Record_Get_DateAdded(user)

            userPoints = self.database.From_User_Record_Get_Points(user)

            secondsSinceArrival = (datetime.datetime.now() - userDate).total_seconds()

            self.highScorers[userName] = [userDate,userPoints,secondsSinceArrival,None,None] 

    def Make_Everyone_Non_Dominated(self):

        for user in self.highScorers:

            self.highScorers[user][3] = False

    def Make_Ago_String(self):

        for userName in self.highScorers:

            userDate   = self.highScorers[userName][0]
            userPoints = self.highScorers[userName][1]

            secondsSinceArrival = math.floor((datetime.datetime.now() - userDate).total_seconds())
            minutesSinceArrival = math.floor(secondsSinceArrival / 60)
            hoursSinceArrival   = math.floor(minutesSinceArrival / 60)
            daysSinceArrival    = (datetime.datetime.now() - userDate).days

            if daysSinceArrival > 1:

                dateString = str(daysSinceArrival) + ' days ago.'

            elif daysSinceArrival == 1:

                dateString = '1 day ago.'

            elif hoursSinceArrival > 1:
 
                dateString = str(hoursSinceArrival) + ' hrs ago.'

            elif hoursSinceArrival == 1:

                dateString = '1 hr ago.'

            elif minutesSinceArrival > 1:

                dateString = str(minutesSinceArrival) + ' mins ago.'

            elif minutesSinceArrival == 1:

                dateString = '1 min ago.'

            elif secondsSinceArrival > 1:

                dateString = str(secondsSinceArrival) + ' secs ago.'

            elif secondsSinceArrival == 1:

                dateString = '1 sec ago.'
            else:
                dateString = '0 sec ago.'

            self.highScorers[userName][4] = dateString

    def Tag_Dominated_Users(self):

        for user1 in self.highScorers:

            user1Points = self.highScorers[user1][1]
            user1Age    = self.highScorers[user1][2]

            for user2 in self.highScorers:

                user2Points = self.highScorers[user2][1]
                user2Age    = self.highScorers[user2][2]

                usersAreDifferent        = user1 != user2

                user2HasLessPoints       = user2Points <= user1Points
                user2IsOlder             = user2Age    >= user1Age

                user2IsDominated         = user2HasLessPoints and user2IsOlder and usersAreDifferent

                if user2IsDominated:

                    self.highScorers[user2][3] = True

    def Save(self):

        plt.savefig('../visualizations/hS.png')
        os.system('mv ../visualizations/hS.png ../visualizations/highScores.png')
        self.fig.clf()

        del self.fig
        del self.ax

        plt.close()

# --------- Main function -------------

database = DATABASE()

hs = HIGH_SCORES(database)

hs.Draw()

hs.Save()

