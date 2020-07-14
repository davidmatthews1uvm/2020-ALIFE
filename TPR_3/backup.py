import re
import socket
import time

# cfg.py
HOST = "irc.twitch.tv"  # the Twitch IRC server
PORT = 6667  # always use port 6667!
NICK = "tpr_bot"  # your Twitch username, lowercase
PASS = ""  # your Twitch OAuth token
CHAN = ""  # the channel you want to join
RATE = (20. / 30.)  # messages per second
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


# bot.py

def Chat_From_User(msg):
    return (msg[0] != ':')


def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG #{} :{}".format(cfg.CHAN, msg))


def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))


def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))


def Initialize():
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
    return s


def Handle_Chat(s):
    response = s.recv(1024).decode("utf-8")

    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)  # return the entire match
        message = CHAT_MSG.sub("", response)

        if (Chat_From_User(message)):
            print(username + ': ' + message)

    time.sleep(1.0 / RATE)


s = Initialize()

while True:
    Handle_Chat(s)