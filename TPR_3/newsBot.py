import random
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

def Reinforcement_From_User(msg):
    return ((msg[0] != ':') and ((msg[1] == 'y') or (msg[1] == 'n')))


def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG #{} :{}".format(CHAN, msg))


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


def Bot_Spawned():
    return (random.randrange(0, 100) < 5)


def Bot_Died():
    return (random.randrange(0, 100) < 5)


def Handle_Chat(s):
    response = s.recv(1024).decode("utf-8")
    username = re.search(r"\w+", response).group(0)  # return the entire match
    message = CHAT_MSG.sub("", response)

    if (Reinforcement_From_User(message)):
        Handle_Reinforcement_From_User(s, username, message)

    time.sleep(1.0 / RATE)


def Handle_Reinforcement_From_User(s, username, message):
    reinforcement = message[1]
    oldProb = random.randrange(1, 99)

    if (reinforcement == 'n'):

        newProb = random.randrange(0, oldProb - 1)
    else:
        newProb = random.randrange(oldProb + 1, 100)

    botIndex = str(random.randrange(100, 1000))
    Send_Response_To_Reinforcement(s, username, oldProb, newProb, botIndex)


def Send_Response_To_Reinforcement(s, username, oldProb, newProb, botIndex):
    message = "@" + username + " just "

    if (oldProb < newProb):
        message = message + "increased "
    else:
        message = message + "decreased "

    message = message + "bot " + botIndex + "'s chance of spawning from "
    message = message + str(oldProb)
    message = message + "% to "
    message = message + str(newProb)
    message = message + "%.\r\n"
    message = 'PRIVMSG ' + CHAN + ' :' + message

    s.send(message.encode("utf-8"))


def Send_Spawn_Message():
    parentIndex = random.randrange(100, 1000)
    childIndex = random.randrange(parentIndex + 1, 1001)

    message = "Bot "
    message = message + str(parentIndex)
    message = message + " just had a baby: bot "
    message = message + str(childIndex) + "."
    # message = message + "\r\n"
    # print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '-->'
    print(message)
    # message = 'PRIVMSG '+CHAN+' :'+message
    # s.send(message.encode("utf-8"))

def Send_Death_Message():
    deadBotIndex = random.randrange(100, 1000)
    message = "Bot " + str(deadBotIndex) + " just died."
    # message = message + "\r\n"
    # print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '-->'

    print(message)
    # message = 'PRIVMSG '+CHAN+' :'+message
    # s.send(message.encode("utf-8"))

# --------------------- Main -------------------------

# s = Initialize()

while True:
    if (Bot_Spawned()):
        Send_Spawn_Message()
    elif (Bot_Died()):
        Send_Death_Message()

    time.sleep(1.0 / RATE)
