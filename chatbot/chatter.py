import math
import sys
import os
import re
import random
import time
from collections import namedtuple

import sys
sys.path.insert(0, '..')
import constants as c

from chatbot.connection         import CONNECTION
from chatbot.help               import HELP
from chatbot.command            import COMMAND
from chatbot.reinforcement      import REINFORCEMENT
from chatbot.speedChange        import SPEED_CHANGE
from chatbot.unlock             import UNLOCK
from chatbot.showAll            import SHOW_ALL
from chatbot.buyBot             import BUY_BOT
from chatbot.stealBot           import STEAL_BOT
from chatbot.unlockEnv          import UNLOCK_ENV
from chatbot.allChat            import ALL_CHAT
from database.database          import DATABASE

class CHAT_BOT():
    def __init__(self):

        self.database = DATABASE() 

        self.Open_Connection()

        self.timeOfLastConnectionReset = time.time()

    def Close_Connection(self):

        self.connection.close_socket()

    def Create_User_If_Necessary(self):

        if not self.database.User_Exists(self.username):
            self.database.Add_User(self.username)
            self.Welcome_New_User()

    def Send_Chat(self):

        chatType = random.randint(0,5)

        if chatType == 0:

            self.Send_Command()

        elif chatType == 1:

            self.Send_Speedup()

        else:
            self.Send_ReinforcementUnlock()

    def Send_Command(self):

        print('*jump')

        self.connection.send_message('*jump')

    def Send_ReinforcementUnlock(self):

        randomColor = random.choice( c.colors )
 
        randomPrefix = random.choice( [ '' , 'u'] )

        randomChat = randomPrefix + randomColor

        print(randomChat)

        self.connection.send_message(randomChat)

    def Send_Speedup(self):

        print('+')

        self.connection.send_message('+')

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

        self.chat_help          = HELP(         self.database, self.connection)
        self.chat_command       = COMMAND(      self.database, self.connection)
        self.chat_reinforcement = REINFORCEMENT(self.database, self.connection)
        self.chat_speedChange   = SPEED_CHANGE( self.database, self.connection)
        self.chat_unlock        = UNLOCK(       self.database, self.connection)
        self.chat_showAll       = SHOW_ALL(     self.database, self.connection)
        self.chat_buyBot        = BUY_BOT(      self.database, self.connection)
        self.chat_stealBot      = STEAL_BOT(    self.database, self.connection)
        self.chat_unlockEnv     = UNLOCK_ENV(   self.database, self.connection)
        self.chat_all           = ALL_CHAT(     self.database, self.connection)

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

    def Respond_If_Reinforcement(self):

        if self.chat_reinforcement.is_valid_message(self.message):
            self.chat_reinforcement.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Show_All(self):

        if self.chat_showAll.is_valid_message(self.message):
            self.chat_showAll.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Speed_Change(self):

        if self.chat_speedChange.is_valid_message(self.message):
            self.chat_speedChange.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Steal_Bot(self):

        if self.chat_stealBot.is_valid_message(self.message):
            self.chat_stealBot.handle_chat_message(self.username, self.message)
            #print('')

    def Respond_If_Unlock(self):

        if self.chat_unlock.is_valid_message(self.message):
            self.chat_unlock.handle_chat_message(self.username, self.message)
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

        
    def Shorten_Message_If_Necessary(self):

        if len( self.message ) > c.longestUserMessage:

            self.message = self.message[:c.longestUserMessage]

    def Welcome_New_User(self):

        msg = "Welcome %s! Typing options for you will appear in stream shortly." % (self.username)
        self.connection.send_message(msg)

    def handle_chat(self):

        # self.Reset_Connection()

        self.Get_Message()

        if not self.message:

            return

        self.Create_User_If_Necessary()

        self.user_dat = self.database.Get_User_Stats(self.username)

        self.Respond_If_Unlock_Env()

        self.Respond_If_Steal_Bot()

        self.Respond_If_Buy_Bot()

        self.Respond_If_Show_All()

        self.Respond_If_Speed_Change()

        self.Respond_If_Command()

        self.Respond_If_Reinforcement()

        self.Respond_If_Unlock()

        self.Respond_If_Help()

        self.Log_Chat()

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

        chatbot.Send_Chat()

        secondsToSleepFor = random.randint(5,30)

        time.sleep(secondsToSleepFor)
