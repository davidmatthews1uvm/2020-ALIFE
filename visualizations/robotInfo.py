import os

import datetime

import constants as c

from database.database import DATABASE

import matplotlib.pyplot as plt

class ROBOT_INFO:

    def __init__(self,primaryRobotIndex):

        self.db = DATABASE()

        self.primaryRobotIndex = primaryRobotIndex

        self.leftEdge = 1000

        self.rightEdge = -1000

        self.topEdge = -1000

        self.bottomEdge = +1000

        self.farLeftMargin = 0.0

        self.leftMargin = 0.49

        self.centerMargin = 0.5

        self.rightMargin = 0.51

        self.topRow = 0.9

        self.rowHeight = 0.095

        self.Compute_B_Index()

    def Draw(self):

        plt.rcParams.update({'font.size': 22})

        self.fig, self.ax = plt.subplots(1)

        self.Draw_Text()

        self.Clean_Up()

    def Draw_Empty(self):

        plt.rcParams.update({'font.size': 22})

        self.fig, self.ax = plt.subplots(1)

        self.Clean_Up()

    def Save(self):

        plt.savefig('../visualizations/rI.png')
        os.system('mv ../visualizations/rI.png ../visualizations/robotInfo.png')
        self.fig.clf()

        del self.fig
        del self.ax

        plt.close()

# -------------- Private methods -----------

    def Clean_Up(self):

        self.ax.set_xticks([])

        self.ax.set_yticks([])

        robotColor = c.colorNames[ self.primaryRobotIndex ]

        rgb = c.colorRGBs[self.primaryRobotIndex]

        self.ax.set_title(robotColor) # ,color=rgb)

    def Compute_B_Index(self):

            robot = self.db.Get_Living_Robot_At_Position(self.primaryRobotIndex)

            robotID = self.db.From_Robot_Record_Get_ID(robot)

            self.BIndex = self.db.Get_B_Index_For_Robot(robotID)

            self.commands = self.db.Get_Commands_Robot_Is_Most_Obedient_To(robotID)

            self.BIndex = 0

            for command in sorted(self.commands, key=self.commands.get, reverse=True):

                numYesVotes = self.commands[command]

                if ( numYesVotes > self.BIndex ):

                    self.BIndex = self.BIndex + 1

    def Draw_Age(self):

        robot = self.db.Get_Living_Robot_At_Position(self.primaryRobotIndex)

        robotCreationDate = self.db.From_Robot_Record_Get_Creation_Date(robot)

        robotCreationDateString = robotCreationDate.strftime("%Y-%m-%d %H:%M:%S")

        robotDate , robotTime = str.split(robotCreationDateString)

        robotYear , robotMonth , robotDay = str.split(robotDate,'-')

        robotHour , robotMinute , robotSecond = str.split(robotTime,':')

        timeOfBirth = datetime.datetime(year=int(robotYear), month=int(robotMonth), day=int(robotDay) , hour=int(robotHour) , minute = int(robotMinute) , second = int(robotSecond))

        robotAge = str(datetime.datetime.now() - timeOfBirth)

        robotAgeSplitAttempted = str.split(robotAge)

        if ( len(robotAgeSplitAttempted) == 1 ):

            robotAgeHour , robotAgeMinute , robotAgeSecond = str.split(robotAge,':')

            plt.text( x = self.leftMargin  , y = self.topRow , s = 'Age:' , horizontalalignment = 'right'  )

            if ( int(robotAgeHour) > 0 ):

                robotAgeHour = str(int(robotAgeHour))

                if int(robotAgeHour) == 1:

                    plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeHour + ' hour. ' , horizontalalignment = 'left'  )
                else:
                    plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeHour + ' hours.' , horizontalalignment = 'left'  )

            elif ( int(robotAgeMinute) > 0 ):

                robotAgeMinute = str(int(robotAgeMinute))

                if int(robotAgeMinute) == 1:

                    plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeMinute + ' minute. ' , horizontalalignment = 'left'  )
                else:
                    plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeMinute + ' minutes.' , horizontalalignment = 'left'  )
            else:

                robotAgeSecond = str(int(float(robotAgeSecond)))

                if int(robotAgeSecond) == 1:

                    plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeSecond + ' second. ' , horizontalalignment = 'left'  )
                else:
                    plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeSecond + ' seconds.' , horizontalalignment = 'left'  )

        else:
            robotAgeDays = robotAgeSplitAttempted[0]

            plt.text( x = self.leftMargin  , y = self.topRow , s = 'Age:' , horizontalalignment = 'right'  )
           
            if int(robotAgeDays) == 1:

                plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeDays + ' day. ' , horizontalalignment = 'left'  )
            else:
                plt.text( x = self.rightMargin , y = self.topRow , s = robotAgeDays + ' days.' , horizontalalignment = 'left'  )

    def Draw_B_Index(self):

            plt.text( x = self.leftMargin  , y = self.topRow - 2 * self.rowHeight , s = 'Score:' , horizontalalignment = 'right'  )

            plt.text( x = self.rightMargin , y = self.topRow - 2 * self.rowHeight , s = str(self.BIndex), horizontalalignment = 'left' , weight='bold' )

    def Draw_Commands(self):

            commandRank = 0

            for command in sorted(self.commands, key=self.commands.get, reverse=True):

                textHeight = self.topRow - (4 + commandRank) * self.rowHeight

                plt.text( x = self.leftMargin  , y = textHeight , s = '!' + command + ':', horizontalalignment = 'right'  )

                if ( commandRank < self.BIndex ):

                    textWeight = 'bold'
                else:
                    textWeight = 'normal'

                yesVotes = str(self.commands[command])

                if ( commandRank > 0 ):

                    plt.text( x = self.rightMargin , y = textHeight , s = yesVotes + ' w ' , horizontalalignment = 'left' , weight = textWeight )

                elif ( self.commands[command] == 1 ):

                    plt.text( x = self.rightMargin , y = textHeight , s = yesVotes + ' win. ' , horizontalalignment = 'left' , weight = textWeight )
                else:
                    plt.text( x = self.rightMargin , y = textHeight , s = yesVotes + ' wins.' , horizontalalignment = 'left' , weight = textWeight )

                commandRank = commandRank + 1

                if self.Reached_Bottom_Of_Window(commandRank):

                    break

                #if self.No_More_Yes_Votes(command):

                #    break

    def Draw_Owner(self):

        robot = self.db.Get_Living_Robot_At_Position(self.primaryRobotIndex)

        ownerID = self.db.From_Robot_Record_Get_Owner_ID(robot)

        if ownerID == -1:

            ownerName = "none."
        else:
            owner = self.db.Get_User_By_ID(ownerID)

            ownerName = self.db.From_User_Record_Get_Name(owner)

        plt.text( x = self.leftMargin  , y = self.topRow - 1 * self.rowHeight , s = 'Owner:' , horizontalalignment = 'right'  )

        plt.text( x = self.rightMargin , y = self.topRow - 1 * self.rowHeight , s = ownerName, horizontalalignment = 'left' )

    def Draw_Text(self):

        self.Draw_Age()

        self.Draw_Owner()

        self.Draw_B_Index()

        self.Draw_Commands()

    def No_More_Yes_Votes(self,command):

        return self.commands[command] == 0

    def Reached_Bottom_Of_Window(self,commandRank):

        return commandRank == 6

