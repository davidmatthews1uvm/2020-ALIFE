import passiveGameConstants as pgc

import time

class CHAT: 

    def __init__(self):

        self.valid = False

        self.chat = input('> ')

        self.Process()

        self.time = time.time()

    def Get_Request(self):

        return self.chatComponents[1]

    def Get_Time(self):

        return self.time

    def Get_User_Name(self):

        return self.chatComponents[0]

    def Is_Valid(self):

        return (isinstance(self.Get_User_Name(), str)) and (self.numChatComponents==2) 

    def Process(self):

        if self.User_Wants_To_Quit():

            exit(0)

        self.chatComponents = str.split(self.chat)

        self.numChatComponents = len( self.chatComponents )

    def Request_Type( self ):

        request = self.Get_Request()

        if self.Is_Steal_Request( request ):

           return pgc.stealRequest

        elif self.Is_Buy_Request( request ):

           return pgc.buyRequest

        elif self.Is_Show_All_Bots_Request( request ):

           return pgc.showAllBotsRequest

        elif self.Is_Speed_Up_Request( request ):

           return pgc.speedUpRequest

        elif self.Is_Slow_Down_Request( request ):

           return pgc.slowDownRequest

        elif self.Is_Command_Request( request ):

           return pgc.commandRequest

        elif self.Is_Positive_Reinforcement_Request( request ):

           return pgc.positiveReinforcementRequest

        elif self.Is_Negative_Reinforcement_Request( request ):

           return pgc.negativeReinforcementRequest

        elif self.Is_Unlock_Bot_Request( request ):

           return pgc.unlockBotRequest

        elif self.Is_Help_Request( request ):

           return pgc.helpRequest

        else:

           return pgc.rawChat

# --------- Private methods ---------------

    def Is_Buy_Request( self , request ):

        if len(request) != 1:

            return False

        return request[0] == 'r'

    def Is_Command_Request(self , request ):

        if len(request) < 2:

            return False

        return request[0] == '!'

    def Is_Help_Request(self, request):

        return request[0] == '?'

    def Is_Negative_Reinforcement_Request(self , request ):

        if len(request) != 2:

            return False

        return (request[0] == 'r') and (request[1] == 'n')

    def Is_Positive_Reinforcement_Request(self , request ):

        if len(request) != 2:

            return False

        return (request[0] == 'r') and (request[1] == 'y')

    def Is_Unlock_Bot_Request(self , request ):

        if len(request) != 2:

            return False

        return (request[0]=='u') and (request[1]=='y')

    def Is_Show_All_Bots_Request( self , request ):

        if len(request) != 3:

            return False

        return (request[0]=='a') and (request[1]=='l') and (request[2]=='l')

    def Is_Slow_Down_Request( self , request ):
    
        if len(request) > 1:

            return False

        return request[0] == '-'

    def Is_Speed_Up_Request( self , request ):

        if len(request) > 1:

            return False

        return request[0] == '+'
 
    def Is_Steal_Request( self , request ):

        if len(request) != 2:

            return False

        return (request[0]=='x') and (request[1]=='r')

    def User_Wants_To_Quit(self):

        return self.chat == 'quit' or self.chat == 'exit'
