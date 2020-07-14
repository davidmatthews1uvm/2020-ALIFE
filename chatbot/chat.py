from abc import ABC, abstractmethod
import os, pickle
import constantsPassiveGame as cpg

import constants as c

class CHAT(ABC):
    """
    Abstract method for parsing and acting on chat messages
    """
    def __init__(self, database, connection):
        super().__init__()
        self.connection = connection
        self.database = database

    @abstractmethod
    def is_valid_message(self, message):
        """
        Checks if the message can be handled by the class.
        Ex. Checks if message is a help request, a reinforcement, a command, or other.
        :param message: The message to evaluate
        :return: True if the message is the class can handle the message, false otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def handle_chat_message(self, username, message):
        """
        Parses the message, writing the appropiate responses to the chat, and updating the database as needed.
        :param username: The user who sent the message
        :param message: The message to parse
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def handle_unlocked_achievements(self, username):
        """
        Handles any achievements unlocked by successfully entering this form of chat.
        :param username: The user who sent the message
        :return: None
        """
        raise NotImplementedError()

    def Print_Cannot_Afford_Message(self,username):

        return username + ", you can't afford that yet."

    def print_response(self,chatFromUser,msg,connection):

        if chatFromUser == "":

            fullMsg = msg
        else:
            fullMsg = chatFromUser + " : " + msg

        self.database.Add_Message(fullMsg)

    def user_can_afford_request(self,username,chatRequest):

        usersPoints = self.database.Get_User_Points(username)

        requestCost = cpg.options[chatRequest][1]

        return usersPoints >= requestCost

    def user_pays_for(self,username,chatRequest):

        usersPoints = self.database.Get_User_Points(username)

        requestCost = cpg.options[chatRequest][1]

        newPoints   = usersPoints - requestCost

        self.database.Set_Points_For_User_By_Name(newPoints,username)
