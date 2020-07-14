import constantsPassiveGame as cpg

from database.database import DATABASE

import datetime

import operator

import os

import pickle

import time

import constants as c

from passiveGame.activeUser import ACTIVE_USER

class ACTIVE_USERS:

    def __init__(self,database):

        self.database = DATABASE()

        self.activeUsers = {}

        self.timeOfLastUsersUpdate = time.time()

    def Draw_To(self,screen):

        row = cpg.numRows - 1

        # Sort users by the number of commands they have entered.

        for user in sorted(self.activeUsers.values(), key=operator.attrgetter('points')):

            if ( row > 0 ):

                user.Draw_To(screen,row)

            row = row - 1

    def Get_Highest_Score(self):

        if self.activeUsers == {}:

            return 0

        return self.Get_Highest_Scoring_User().points

    def Get_Max_Pts_And_Pts_Per_Sec(self):

        maxPts    = 0.0   
        ptsPerSec = 0.1

        for user in self.activeUsers:

            if self.activeUsers[user].Get_Points() > maxPts:

                maxPts = self.activeUsers[user].Get_Points()

                ptsPerSec = self.activeUsers[user].Get_Pts_Per_Sec()

        return maxPts , ptsPerSec

    def Print(self):

        for user in self.activeUsers:

            self.activeUsers[user].Print()

    def Update(self):

        self.Update_Users()

        self.Update_Points()

# -------------- Private methods ---------------

    def File_Exists(self,fileName):

        return os.path.isfile(fileName) 

    def Find_Active_Users(self):

        self.activeUsers = {}

        userMustHaveChattedSinceThisTime = time.time() - cpg.inactivateUserAfter

        userMustHaveChattedSinceThisTime = datetime.datetime.fromtimestamp( userMustHaveChattedSinceThisTime )

        recentChat = self.database.Get_Chat_Entered_Since( userMustHaveChattedSinceThisTime )

        if not recentChat:

            return

        for chat in recentChat:

            userID       = self.database.From_ChatEntries_Record_Get_UserID(chat)
            user         = self.database.Get_User_By_ID(userID)
            username     = self.database.From_User_Record_Get_Name(user)
            points       = self.database.From_User_Record_Get_Points(user)
            pointsPerSec = self.database.From_User_Record_Get_PointsPerSec(user)

            if username not in self.activeUsers:

                self.activeUsers[username] = ACTIVE_USER( userID , username , points , pointsPerSec )

            datetimeOfRecentChat   = self.database.From_ChatEntries_Record_Get_Date(chat)

            self.activeUsers[username].Update_Datetime_Of_Most_Recent_Chat(datetimeOfRecentChat)

    def Get_Highest_Scoring_User(self):

        rankedUsers = sorted(self.activeUsers.values(), key=operator.attrgetter('points'), reverse = True)

        return rankedUsers[0]

    def Update_Points(self):

        for user in self.activeUsers:

            self.activeUsers[user].Update_Points()

    def Update_Users(self):

        secondsSinceLastUsersUpdate = time.time() - self.timeOfLastUsersUpdate

        if secondsSinceLastUsersUpdate > cpg.timeBetweenUsersUpdates:

            self.Find_Active_Users()

            self.timeOfLastUsersUpdate = time.time()
