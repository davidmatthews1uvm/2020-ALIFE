import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class SHOW_ALL(CHAT):
    """
    Class to process requests to show all bots. 
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid show all request 
        :param message: The message to evaluate
        :return: True if the message is a valid show all, false otherwise.
        """
        return message == "all"

    def handle_chat_message(self, username, message):
        """
        stores the request to show all and sends a confirmation to the user.
        """
        if not self.user_can_afford_request(username,cpg.showAllBotsRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        elif self.Some_Bots_Are_Locked():

            msg = "Sorry "+username+", some bots are still locked."
        else:
            self.user_pays_for(username,cpg.showAllBotsRequest)
            self.database.Add_Show_All_Request(username)
            msg = self.show_all_response(username)

        self.print_response(message,msg,self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# ---------------- Private methods ------------------------

    def show_all_response(self,username):

        return username + ", all bots will be shown shortly." 

    def Some_Bots_Are_Locked(self):

        if self.database.Get_Locked_Robots():

            return True
        else:
            return False
