import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class UNLOCK_ENV(CHAT):
    """
    Class to process all chat messages requesting unlocking of environments.
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid unlock request 
        :param message: The message to evaluate
        :return: True if the message is a valid unlock, false otherwise.
        """
        if not message:
            return False
        if len(message) != 2:
            return False
        return message[0].lower()=='u' and message[1] in c.ENVIRONMENT_NUMBERS_AS_CHARS

    def handle_chat_message(self, username, message):
        """
        stores the reinforcement and sends a confirmation to the user.
        """
        unlock     = message[0].lower()
        envNumber = int(message[1])

        if not self.user_can_afford_request(username,cpg.unlockEnvRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        elif self.Env_Is_Locked(envNumber):

            self.user_pays_for(username,cpg.unlockEnvRequest)
            self.Unlock_Environment(envNumber)
            msg = self.unlock_response(envNumber,username)

        else:
            msg = username + ", environment " + str(envNumber) + " is already unlocked."

        self.print_response(message, msg, self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# --------------- Private methods ----------------------

    def unlock_response(self, envNumber, username):
        return "environment "+str(envNumber)+" has been unlocked by " + username + "! It will appear shortly."

    def Env_Is_Locked(self,envNumber):

        env = self.database.Get_Environment(envNumber)

        if env == []:

            return False

        return self.database.From_Environment_Record_Get_Locked_Status(env)

    def Unlock_Environment(self,envNumber):

        self.database.Unlock_Environment(envNumber)

