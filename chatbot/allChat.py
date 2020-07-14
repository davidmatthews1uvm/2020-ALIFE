from chatbot.chat import CHAT

class ALL_CHAT(CHAT):
    """
    Class to handle all chat messages
    """
    def is_valid_message(self, message):
        """
        Every message can be logged to the database.
        :return: True
        """
        return True

    def handle_chat_message(self, username, message):
        """
        Logs the given message and username to the database
        """
        self.database.Add_Chat_Message(message, username)

    def handle_unlocked_achievements(self,username):

        pass

    def user_can_afford_this(self):

        return True
