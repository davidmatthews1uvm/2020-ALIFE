import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class SHOW_BEST(CHAT):
    """
    Class to process requests to show the best bot. 
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid show best request 
        :param message: The message to evaluate
        :return: True if the message is a valid show best, false otherwise.
        """
        return message == "best"

    def handle_chat_message(self, username, message):
        """
        stores the request to show best and sends a confirmation to the user.
        """
        if not self.user_can_afford_request(username,cpg.showBestBotRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        elif self.Some_Bots_Are_Locked():

            msg = "Sorry "+username+", some bots are still locked."
        elif self.B_Index_Not_High_Enough():

            msg = "Sorry "+username+", the best bot will only be available for viewing when it's beaten at least two other bots for each of two commands."

        else:
            self.user_pays_for(username,cpg.showBestBotRequest)
            self.database.Add_Show_Best_Request(username)
            msg = self.show_best_response(username)

        self.print_response(message,msg,self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# ---------------- Private methods ------------------------

    def show_best_response(self,username):

        return username + ", the best bot will be shown shortly." 

    def B_Index_Not_High_Enough(self):

        colorIndex, BIndex = self.database.Get_Color_Index_And_Highest_B_Index_Among_Living_Robots()

        return BIndex < 2
 
    def Some_Bots_Are_Locked(self):

        if self.database.Get_Locked_Robots():

            return True
        else:
            return False
