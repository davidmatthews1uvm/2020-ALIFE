import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class BUY_BOT(CHAT):
    """
    Class to process all requests to buy a bot.
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid buy request 
        :param message: The message to evaluate
        :return: True if the message is a valid buy request, false otherwise.
        """
        if len(message) != 2:
            return False
        return message[0].lower() in ['b'] and message[1].lower() in c.colors

    def handle_chat_message(self, username, message):
        """
        stores the buy request and sends a confirmation to the user.
        """
        color = message[1].lower()

        [evaluationID, robotID] = self.database.Get_Most_Recent_Evaluation_With_Bot_Color(color)

        self.database.Add_Buy_Request(robotID, username)

        if not self.user_can_afford_request(username,cpg.buyRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        elif evaluationID == -1:

            msg = "Sorry {}, a robot with that color does not exist or has not been shown yet. ".format(username)

        elif self.database.Bot_Is_Dead(robotID):

            msg = "Sorry " + username + ", there is no " + c.colorNameDict[color] + " bot now."

        elif self.Bot_Is_Locked(color):

            msg = "Sorry " + username + ", " + c.colorNameDict[color] + " is locked."

        elif self.Bot_Is_Already_Owned(robotID):

            ownerName = self.Get_Owner_Of(robotID)

            if username == ownerName:

                msg = username + ", you already own " + c.colorNameDict[color] + "."
            else:
                msg = "Sorry " + username + ", " + c.colorNameDict[color] + " is already owned by " + self.Get_Owner_Of(robotID) + "."

        else:
            self.user_pays_for(username,cpg.buyRequest)
            self.Honor_Buy_Request(username,robotID)
            msg = self.buy_request_response(username, color)

        self.print_response(message,msg,self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# -------------------- Private methods ----------------------

    def Bot_Is_Already_Owned(self,robotID):

        bot = self.database.Get_Robot_By_ID(robotID)

        ownerID = self.database.From_Robot_Record_Get_Owner_ID(bot)

        return ownerID != -1

    def Bot_Is_Locked(self,colorChar):

        colorIndex = c.colors.index(colorChar)

        return self.database.Robot_With_This_Color_Index_Is_Locked(colorIndex)

    def buy_request_response(self, username, colorChar):

        colorName = c.colorNameDict[colorChar]

        return username + " bought " + colorName + "!" 

    def Get_Owner_Of(self,robotID):

        bot = self.database.Get_Robot_By_ID(robotID)

        ownerID = self.database.From_Robot_Record_Get_Owner_ID(bot)

        owner = self.database.Get_User_By_ID(ownerID)

        ownerName = self.database.From_User_Record_Get_Name(owner)

        return ownerName

    def Honor_Buy_Request(self,username,robotID):

        user = self.database.Get_User_By_Name(username)

        userID = self.database.From_User_Record_Get_Id(user)

        self.database.Set_Owner_Of_Robot(userID,robotID)
 
        buyRequest = self.database.Get_Most_Recent_Buy_Request()

        buyRequestID = self.database.From_Buy_Request_Record_Get_ID(buyRequest)

        self.database.Set_Buy_Request_Successful_By_ID(buyRequestID)
