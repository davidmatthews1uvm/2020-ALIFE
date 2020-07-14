import string
import socket
import sys
import os
import time
import datetime

sys.path.insert(0, "..")
import constants as c


class CONNECTION:
    """
    This class is used to create a connection to the chatbot and communicate with it. The method
    handle_incoming() at the bottom is where messages are received from the chatbot and then their
    corresponding CHAT objects created.
    """
    def __init__(self, channel, host, port, identity):
        self.channel = channel
        self.host = host
        self.port = port
        self.identity = identity
        self.s = None

    def close_socket(self):

        self.s.close()

    def connect(self, oauth):
        """
        Initializes a connection to twitch, and joins the given twitch channel.
        :return:
        """
        self.open_socket(oauth)
        self.join_room()

    def open_socket(self, password):
        self.s = socket.socket()
        self.s.connect((self.host, self.port))
        self.s.send(("PASS " + password + "\r\n").encode("utf-8"))
        self.s.send(("NICK " + self.identity + "\r\n").encode("utf-8"))
        self.s.send(("JOIN #" + self.channel + "\r\n").encode("utf-8"))


    def send_message(self, message):
        messageTemp = "PRIVMSG #" + self.channel + " :" + message + "\r\n"
        self.s.send((messageTemp).encode("utf-8"))
        # print("Sent message to host: " + messageTemp)

    def join_room(self):
        readbuffer = ""
        loading = True
        while loading:
            readbuffer = readbuffer + (self.s.recv(1024)).decode()
            temp = str.split(readbuffer, "\n")
            readbuffer = temp.pop()

            for line in temp:
                loading = self.loading_complete(line)

        # self.send_message("Successfully joined chatroom")

    def loading_complete(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True

    def ping_from_server(self, response):
        pinged = "PING :tmi.twitch.tv" in response
        return pinged

    def pong_back(self):
        self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        # print("I ponged back!")

    def get_user(self, line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def get_message(self, line):
        separate = line.split(":", 2)
        message = separate[2]
        return message

    def get_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def get_user_message(self):

        # Most of the time is spent on the following line waiting to hear from Twitch.
        readbuffer = self.s.recv(1024).decode()

        string_list = str.split(readbuffer, "\n")
        readbuffer = string_list.pop()

        for line in string_list:
            if self.ping_from_server(line):
                # print("Twitch pinged me at " + self.get_datetime() + ".")
                self.pong_back()
                break

            username = self.get_user(line)
            message = self.get_message(line).rstrip()
            return (username, message)

        return(None,None)
