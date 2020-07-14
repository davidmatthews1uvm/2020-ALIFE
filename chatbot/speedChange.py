import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class SPEED_CHANGE(CHAT):
    """
    Class to process all reinforcement chat messages
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid speed change request 
        :param message: The message to evaluate
        :return: True if the message is a valid speed change request, false otherwise.
        """
        if len(message) != 1:
            return False
        return message[0] in ['+', '-']

    def handle_chat_message(self, username, message):
        """
        stores the speed change request and sends a confirmation to the user.
        """
        speedChangeRequest = message[0]

        currentEvaluation = self.database.Get_Current_Evaluation()

        if not currentEvaluation:

            return

        currentSpeed = self.database.From_Evaluation_Record_Get_Speed(currentEvaluation)

        if not self.user_can_afford_request(username,cpg.speedUpRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        elif speedChangeRequest == '+' and self.At_Maximum_Speed(currentSpeed):

            msg = username + ", the sim cannot run faster than " + str(c.MAXIMUM_SPEED) + "x real time."

        elif speedChangeRequest == '-' and self.At_Minimum_Speed(currentSpeed):

            msg = username + ", the sim cannot run slower than " + str(c.MINIMUM_SPEED) + "x real time."

        else:
            self.user_pays_for(username,cpg.speedUpRequest)
            self.database.Add_Speed_Change_Request(speedChangeRequest,username)
            msg = self.speed_change_response(username, speedChangeRequest)

        self.print_response(message,msg,self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# -------------- Private methods -----------------------

    def speed_change_response(self, username, speedChangeRequest):

        msg = username + ", the simulations will "
        if (speedChangeRequest == '+'):
            msg = msg + "speed up "
        else:
            msg = msg + "slow down "

        msg = msg + "shortly."

        return msg

    def At_Maximum_Speed(self,currentSpeed):

        return currentSpeed == c.MAXIMUM_SPEED

    def At_Minimum_Speed(self,currentSpeed):

        return currentSpeed == c.MINIMUM_SPEED
