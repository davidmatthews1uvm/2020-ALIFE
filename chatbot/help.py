import constants as c

from chatbot.chat import CHAT 

class HELP(CHAT):
    """
    Class to handle all help requests.
    """
    def __init__(self, database, connection):
        super().__init__(database, connection)

    def is_valid_message(self, message):
        """
        Checks if the message is a valid help command.
        :param message: The message to evaluate
        :return: True if the message is a valid help command, false otherwise.
        """
        return message in c.validHelpRequests

    def handle_chat_message(self, username, message):
        """
        Parses the message and serves the correct help response.
        """

        if message == "?":
            response = ""
            for helpRequest in c.validHelpRequests:
                if not helpRequest == "?":

                    response = response + helpRequest + " "

            self.print_response(message,response,self.connection)

        elif message == "?mybots": 

            self.Show_User_Her_Bots(username)

        else:
            response = c.validHelpRequests[message]

            self.print_response(message,response,self.connection)

    def handle_unlocked_achievements(self,username):

        pass 

    # ------------------ Private methods ------------------

    def Add_Carriage_Return_To(self,response):

        response = response + "\n"

        response = response.rjust(c.WIDTH_OF_LEFTHAND_CHATBOT_OUTPUT)

        response = response + " : "

        return response

    def Find_Her_Bots(self,username):

        user = self.database.Get_User_By_Name(username)

        userID = self.database.From_User_Record_Get_Id(user)

        self.bots = self.database.Get_Robots_Owned_By(userID)

    def get_stats(self, username):
        ttl_robots = self.database.Total_Robots()
        ttl_users = self.database.Total_Users()

        if (ttl_users == 1):
            user_string = "user"
        else:
            user_string = "users"

        return "%s robots have been spawned so far. They have received feedback " \
               "from %s %s. " % (ttl_robots, ttl_users, user_string)

    def get_commands_help_page(self):
        return "We are sending commands to robots in a way which helps to preserve the relative " \
               "meaning of different commands. This system’s vocabulary is large but does not include" \
               "every possible combination of letters. For more information about how we are sending the" \
               "commands to robots go to https://en.m.wikipedia.org/wiki/Word2vec"

    def Show_User_Her_Bots(self,username):

        self.Find_Her_Bots(username)

        self.Sort_Her_Bots()

        self.Show_Her_Bots(username)

    def Sort_Her_Bots(self):

        herBots = []

        self.herScore = 0

        for bot in self.bots:

            botID              = self.database.From_Robot_Record_Get_ID(bot)
            botColorIndex      = self.database.From_Robot_Record_Get_Color_Index(bot)
            botAlive           = self.database.From_Robot_Record_Get_Alive_Status(bot)

            botBIndex          = self.database.Get_B_Index_For_Robot(botID)

            self.herScore      = self.herScore + botBIndex

            herBots.append( [botID,botColorIndex,botAlive,botBIndex] )

        self.sortedByDescendingBIndex = sorted(herBots, key=lambda tup: tup[3] , reverse=True)

    def Show_Her_Bots(self,username):

        numOwnedBots = len(self.sortedByDescendingBIndex)

        if numOwnedBots == 0:

            msg = username+", you do not own any bots yet."
        else:

            msg = username+"'s bots' scores:"

            msg = msg + "["

            self.botIndex = 0

            for bot in self.sortedByDescendingBIndex:

                msg = msg + self.Show_This_Bot(bot,numOwnedBots)

            msg = msg + "] "

            msg = msg + username+"'s score: "

            self.botIndex = 0

            for bot in self.sortedByDescendingBIndex:

                msg = msg + self.Sum_This_Bot(bot,numOwnedBots)

            msg = msg + "="

            msg = msg + str(self.herScore) + "."

        self.print_response("?mybots",msg,self.connection)

    def Show_This_Bot(self,bot,numOwnedBots):

        botID         = bot[0]
        botColorIndex = bot[1]
        botAlive      = bot[2]
        bIndex        = bot[3]

        msg = str(bIndex)

        if self.botIndex < (numOwnedBots-1):

            msg = msg + ","

        self.botIndex = self.botIndex + 1

        return msg

    def Sum_This_Bot(self,bot,numOwnedBots):

        botID         = bot[0]
        botColorIndex = bot[1]
        botAlive      = bot[2]
        bIndex        = bot[3]

        msg = str(bIndex)

        if self.botIndex < (numOwnedBots-1):

            msg = msg + "+"

        self.botIndex = self.botIndex + 1

        return msg
