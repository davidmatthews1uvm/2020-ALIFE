import datetime
import math
import sys
import os
import pickle
import re
import time
from collections import namedtuple

import sys
sys.path.insert(0, '..')
import constants as c
import constantsPassiveGame as cpg

from chatbot.connection         import CONNECTION

from chatbot.unlockEnv          import UNLOCK_ENV
from chatbot.stealBot           import STEAL_BOT
from chatbot.buyBot             import BUY_BOT
from chatbot.showAll            import SHOW_ALL
from chatbot.speedChange        import SPEED_CHANGE
from chatbot.command            import COMMAND
from chatbot.showBest           import SHOW_BEST
from chatbot.reinforcement      import REINFORCEMENT
from chatbot.help               import HELP
from chatbot.infoReward         import INFO_REWARD

from chatbot.allChat            import ALL_CHAT
from database.database          import DATABASE

class CHAT_BOT():
    def __init__(self):

        self.database = DATABASE() 

        self.Open_Connection()

        self.timeOfLastConnectionReset = time.time()

    def Close_Connection(self):

        self.connection.close_socket()

    def Create_User_Or_Update_Points(self):

        if not self.database.User_Exists(self.username):
            self.database.Add_User(self.username)
            self.Welcome_New_User()
        else:
            self.Update_Points()

    def Get_Message(self):

        self.username, self.message = self.connection.get_user_message()

        if self.username and self.message:

            self.Shorten_Message_If_Necessary()

    def Log_Chat(self):

        self.chat_all.handle_chat_message(self.username, self.message)

    def Open_Connection(self):

        file      = open("../credentials.credentials", "r")
        oauth     = file.readline().rstrip()
        channel   = file.readline().rstrip()
        host      = "irc.twitch.tv"
        port      = 6667
        identity  = "TPR_Chatbot"
        self.rate = 20./30.

        self.connection = CONNECTION(channel, host, port, identity)
        self.connection.connect(oauth)

        self.chat_help          = HELP(          self.database, self.connection)
        self.chat_command       = COMMAND(       self.database, self.connection)
        self.chat_reinforcement = REINFORCEMENT( self.database, self.connection)
        self.chat_speedChange   = SPEED_CHANGE(  self.database, self.connection)
        self.chat_showAll       = SHOW_ALL(      self.database, self.connection)
        self.chat_showBest      = SHOW_BEST(     self.database, self.connection)
        self.chat_buyBot        = BUY_BOT(       self.database, self.connection)
        self.chat_stealBot      = STEAL_BOT(     self.database, self.connection)
        self.chat_unlockEnv     = UNLOCK_ENV(    self.database, self.connection)
        self.chat_all           = ALL_CHAT(      self.database, self.connection)
        self.chat_infoReward    = INFO_REWARD(   self.database, self.connection)

    def Print_To_Screen(self):

        print(self.username, self.message)

    def Respond_If_Buy_Bot(self):

        if self.chat_buyBot.is_valid_message(self.message):
            self.chat_buyBot.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Command(self):

        if self.chat_command.is_valid_message(self.message):
            self.chat_command.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Help(self):

        if self.chat_help.is_valid_message(self.message):
            self.chat_help.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Info_Reward(self):
        if self.chat_infoReward.is_valid_message(self.message):
            self.chat_infoReward.handle_chat_message(self.username, self.message)

    def Respond_If_Reinforcement(self):

        if self.chat_reinforcement.is_valid_message(self.message):
            self.chat_reinforcement.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Show_All(self):

        if self.chat_showAll.is_valid_message(self.message):
            self.chat_showAll.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Show_Best(self):

        if self.chat_showBest.is_valid_message(self.message):
            self.chat_showBest.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Speed_Change(self):

        if self.chat_speedChange.is_valid_message(self.message):
            self.chat_speedChange.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Steal_Bot(self):

        if self.chat_stealBot.is_valid_message(self.message):
            self.chat_stealBot.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Unlock_Env(self):

        if self.chat_unlockEnv.is_valid_message(self.message):
            self.chat_unlockEnv.handle_chat_message(self.username, self.message)
            #print('')

    def Reset_Connection(self):

        secondsSinceLastConnectionReset = time.time() - self.timeOfLastConnectionReset

        if secondsSinceLastConnectionReset > c.timeBetweenConnectionResets:

            self.Close_Connection()

            self.Open_Connection()

            self.timeOfLastConnectionReset = time.time()

    def Seconds_Since_Last_Chat(self):

        userID = self.database.Get_User_ID(self.username)

        mostRecentChat = self.database.Get_Most_Recent_Chat_From_User(int(userID))

        datetimeOfMostRecentChat = self.database.From_ChatEntries_Record_Get_Date(mostRecentChat)

        datetimeSinceMostRecentChat = datetime.datetime.now() - datetimeOfMostRecentChat

        return datetimeSinceMostRecentChat.total_seconds()
        
    def Shorten_Message_If_Necessary(self):

        if len( self.message ) > c.longestUserMessage:

            self.message = self.message[:c.longestUserMessage]

    def Update_Points(self):

        secondsSinceLastChat = self.Seconds_Since_Last_Chat()

        if secondsSinceLastChat > cpg.inactivateUserAfter:

            return

        userID = self.database.Get_User_ID(self.username)

        user = self.database.Get_User_By_ID(userID)

        points = self.database.From_User_Record_Get_Points(user)

        ptsPerSec = self.database.From_User_Record_Get_PointsPerSec(user)

        points = points + ptsPerSec * secondsSinceLastChat 

        self.database.Set_Points_For_User_By_ID(points,userID)

    def Welcome_New_User(self):

        msg = "Welcome %s! Typing options for you will appear in stream shortly." % (self.username)
        self.connection.send_message(msg)

    def handle_chat(self):

        # self.Reset_Connection()

        self.Get_Message()

        if not self.message:

            return

        self.Create_User_Or_Update_Points()

        self.user_dat = self.database.Get_User_Stats(self.username)

        self.Log_Chat()

        self.Respond_If_Unlock_Env()

        self.Respond_If_Steal_Bot()

        self.Respond_If_Buy_Bot()

        self.Respond_If_Show_All()

        self.Respond_If_Speed_Change()

        self.Respond_If_Command()

        self.Respond_If_Show_Best()

        self.Respond_If_Reinforcement()

        self.Respond_If_Help()

        self.Respond_If_Info_Reward()
        
        # self.Print_To_Screen()

        # time.sleep(self.rate)

if __name__ == "__main__":
    """
    Script to start the chatbot. First credentials are read in from the credentials.credentials file,
    then a chatbot object is created, and it is put into it's handle_chat() loop.
    * The CONNECTION class is used for dealing with the connection to twitch,
    * The Chat classes are used to parse user chat, respond to messages, and update the database
    """

    file = open("../credentials.credentials", "r")
    oauth = file.readline().rstrip()
    channel = file.readline().rstrip()

    chatbot = CHAT_BOT()

    while True:

        chatbot.handle_chat()
