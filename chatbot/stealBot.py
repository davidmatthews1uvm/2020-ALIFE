import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class STEAL_BOT(CHAT):
    """
    Class to process all requests to steal a bot.
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid steal request 
        :param message: The message to evaluate
        :return: True if the message is a valid steal request, false otherwise.
        """
        if len(message) != 2:
            return False
        return message[0].lower() in ['s'] and message[1].lower() in c.colors

    def handle_chat_message(self, username, message):
        """
        stores the steal request and sends a confirmation to the user.
        """
        color = message[1].lower()

        [evaluationID, robotID] = self.database.Get_Most_Recent_Evaluation_With_Bot_Color(color)

        self.database.Add_Steal_Request(robotID, username)

        if not self.user_can_afford_request(username,cpg.stealRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        elif evaluationID == -1:

            msg = "Sorry {}, a robot with that color does not exist or has not been shown yet. ".format(username)

        elif self.database.Bot_Is_Dead(robotID):

            msg = "Sorry " + username + ", there is no " + c.colorNameDict[color] + " bot now."

        elif self.Bot_Is_Locked(color):

            msg = "Sorry " + username + ", " + c.colorNameDict[color] + " is locked."

        elif self.User_Already_Owns_This_Bot(username,robotID):

            msg = username + ", you already own " + c.colorNameDict[color] + "."

        else:
            self.user_pays_for(username,cpg.stealRequest)
            msg = self.steal_request_response(username, color, robotID)
            self.Honor_Steal_Request(username,robotID)

        self.print_response(message,msg,self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# -------------------- Private methods ----------------------

    def Bot_Is_Locked(self,colorChar):

        colorIndex = c.colors.index(colorChar)

        return self.database.Robot_With_This_Color_Index_Is_Locked(colorIndex)

    def steal_request_response(self, username, colorChar, robotID):

        colorName = c.colorNameDict[colorChar]

        return username + " stole " + colorName + " from " + self.Get_Owner_Of(robotID) + "!" 

    def Get_Owner_Of(self,robotID):

        bot = self.database.Get_Robot_By_ID(robotID)

        ownerID = self.database.From_Robot_Record_Get_Owner_ID(bot)

        if ownerID == -1:

            return "no one"

        owner = self.database.Get_User_By_ID(ownerID)

        ownerName = self.database.From_User_Record_Get_Name(owner)

        return ownerName

    def Honor_Steal_Request(self,username,robotID):

        user = self.database.Get_User_By_Name(username)

        userID = self.database.From_User_Record_Get_Id(user)

        self.database.Set_Owner_Of_Robot(userID,robotID)
 
        stealRequest = self.database.Get_Most_Recent_Steal_Request()

        stealRequestID = self.database.From_Steal_Request_Record_Get_ID(stealRequest)

        self.database.Set_Steal_Request_Successful_By_ID(stealRequestID)

    def User_Already_Owns_This_Bot(self,username,robotID):

        user = self.database.Get_User_By_Name(username)

        userID = self.database.From_User_Record_Get_Id(user)

        bot = self.database.Get_Robot_By_ID(robotID)

        ownerID = self.database.From_Robot_Record_Get_Owner_ID(bot)

        return userID == ownerID
