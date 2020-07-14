import constantsPassiveGame as cpg

from chatbot.chat import CHAT

class COMMAND(CHAT):
    """
    Class to process all command messages
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid command to send to the bots.
        i.e. if the message starts with a "!".
        :param message: The message to evaluate
        :return: True if the message is a command, False otherwise.
        """
        return message[0] == "*"

    def handle_chat_message(self, username, message):
        """
        If command is new, checks if it is in our vocab.
        If not, sends error to user.
        else, creates command if needed, and upvotes the command in the database.
        """
        command = message[1:]

        new_command = self.database.Command_Is_New(command)
        vec_avail = False
        if new_command:
            vec_avail, invalid_words = self.database.Try_Get_Command_Vector_Encoding(command)
        else:
            vec_avail, invalid_words = True, None

        if (not vec_avail):
            msg = self.command_not_found_response(username, invalid_words)

        elif self.Command_Contains_Quotes(command):

            msg = self.Print_No_Quotes_Message(username)

        elif not self.user_can_afford_request(username,cpg.commandRequest):

            msg = self.Print_Cannot_Afford_Message(username)

        else:
            self.user_pays_for(username,cpg.commandRequest)
            self.database.Add_Command(command, username)
            msg = self.command_receipt_response(username)

        self.print_response(message,msg,self.connection)

    def handle_unlocked_achievements(self,username):

        pass

# ------------- Private methods --------------------

    def Command_Contains_Quotes(self, command):

        containsSingleQuote = "'" in command

        containsDoubleQuote = '"' in command

        return containsSingleQuote or containsDoubleQuote
 
    def command_receipt_response(self, username):
        return "Thanks {}. Your command will be sent to the robots shortly. ".format(username)

    def command_not_found_response(self, username, invalid_words):

        sent_words = {}
        words_to_send = []

        for word in invalid_words:
            if word in sent_words:
                continue
            else:
                sent_words[word] = 1
                words_to_send.append(word)

        if len(words_to_send) == 1:
            not_in_vocab = "\"" + invalid_words[0] + "\""

            return "%s, the word %s is not in our vocabulary. Please try again. For more information please type ?commands." %(username, not_in_vocab)
        else:
            not_in_vocab = "\"" + words_to_send[0] + "\""
            for word in words_to_send[1:]:
                not_in_vocab += ", \"" + word + "\""
            return "%s, the words %s are not in our vocabulary. Please try again. For more information please type ?commands." %(username, not_in_vocab)

    def Print_No_Quotes_Message(self,username):

        return username + ", commands cannot contain single or double quotes."
