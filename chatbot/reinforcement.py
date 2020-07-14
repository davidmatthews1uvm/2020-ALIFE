import constantsPassiveGame as cpg

import constants as c

from chatbot.chat import CHAT

class REINFORCEMENT(CHAT):
    """
    Class to process all reinforcement chat messages
    """
    def is_valid_message(self, message):
        """
        Checks if the message is a valid reinforcement command
        :param message: The message to evaluate
        :return: True if the message is a valid reinforcement, false otherwise.
        """
        if len(message) != 1:
            return False
        return message[0].lower() in c.colors

    def handle_chat_message(self, username, message):
        """
        stores the reinforcement and sends a confirmation to the user.
        """
        color = message[0].lower()

        [self.evaluationID, self.robotID] = self.database.Get_Most_Recent_Evaluation_With_Bot_Color(color)

        reinforcementSuccessful = False

        if not self.user_can_afford_request(username,cpg.aggressorReinforcementRequest):

            msg = self.Print_Cannot_Afford_Message(username)

            self.print_response(message,msg,self.connection)

        elif self.evaluationID == -1:

            msg = "Sorry {}, a robot with that color does not exist or has not been shown yet. ".format(username)
           
            self.print_response(message,msg,self.connection)

        elif self.database.Bot_Is_Dead(self.robotID):

            msg = "Sorry " + username + ", there is no " + c.colorNameDict[color] + " bot now."

            self.print_response(message,msg,self.connection)

        elif self.Bot_Is_Locked(color):

            msg = "Sorry " + username + ", " + c.colorNameDict[color] + " is locked."

            self.print_response(message,msg,self.connection)

        elif self.Bot_Just_Involved_In_Reproduction_Event():

            msg = "Sorry " + username + ", " + c.colorNameDict[color] + " cannot be rewarded because it was just involved in a reproduction event."

            self.print_response(message,msg,self.connection)

        elif self.Bot_Just_Involved_In_Simulation_Of_All():

            msg = "Sorry " + username + ", " + c.colorNameDict[color] + " cannot be rewarded because it was just shown with all other bots."

            self.print_response(message,msg,self.connection)

        elif self.Bot_Just_Involved_In_Simulation_Of_Best():

            msg = "Sorry " + username + ", " + c.colorNameDict[color] + " cannot be rewarded because it was just shown as the best bot."

            self.print_response(message,msg,self.connection)

        else:
            reinforcementSuccessful = True

            self.Handle_Positive_Reinforcement(username,color,message)

            losingColor = self.Handle_Negative_Reinforcement(username,message)

            if not losingColor:

                return

            #winningColor = c.colorNameDict[color]

            #losingColor  = c.colorNameDict[losingColor]

            #msg = "+1 yes to " + winningColor + " (and +1 no to " + losingColor + ") because "+username+" said "+winningColor+" was better at "+self.commandStr+" than "+losingColor+"."

            #self.print_response(message,msg,self.connection)


        if reinforcementSuccessful:

            self.handle_unlocked_achievements(username,'y',color)

    def handle_unlocked_achievements(self,username,reinforcement,colorChar):

        if self.First_Reinforcement_From(username):

            self.First_Reinforcement_Achievement_Unlocked(username)

        if self.First_Reinforcement_To_Bot(username):

            self.First_Reinforcement_To_Bot_Achievement_Unlocked(username,colorChar)

        if self.Reinforcement_Agrees_With_Crowd_Majority(username,reinforcement):

            self.Reinforcement_Agrees_With_Crowd_Majority_Achievement_Unlocked(username)

        if self.Command_Proposed_By_Another_Collected_A_Yes_Vote(reinforcement):

            self.Command_Proposed_By_Another_Collected_A_Yes_Vote_Achievement_Unlocked(username)
        
# -------------------- Private methods ----------------------

    def Bot_Is_Locked(self,colorChar):

        colorIndex = c.colors.index(colorChar)

        return self.database.Robot_With_This_Color_Index_Is_Locked(colorIndex)

    def Bot_Just_Involved_In_Reproduction_Event(self):

        evaluation = self.database.Get_Evaluation_Where_ID_Equals(self.evaluationID)

        simulationType = self.database.From_Evaluation_Record_Get_Simulation_Type(evaluation)

        return simulationType == c.SIMULATE_BIRTH or simulationType == c.SIMULATE_DEATH

    def Bot_Just_Involved_In_Simulation_Of_All(self):

        evaluation = self.database.Get_Evaluation_Where_ID_Equals(self.evaluationID)

        simulationType = self.database.From_Evaluation_Record_Get_Simulation_Type(evaluation)

        return simulationType == c.SIMULATE_ALL

    def Bot_Just_Involved_In_Simulation_Of_Best(self):

        evaluation = self.database.Get_Evaluation_Where_ID_Equals(self.evaluationID)

        simulationType = self.database.From_Evaluation_Record_Get_Simulation_Type(evaluation)

        return simulationType == c.SIMULATE_BEST

    def Command_Proposed_By_Another(self):

        uniqueCommand = self.database.Get_Unique_Command_By_String(self.commandStr)

        initialProposerID = self.database.From_UniqueCommand_Record_Get_UserID(uniqueCommand)

        commandProposedByAUser = initialProposerID > -1

        commandProposedByAnother = initialProposerID != self.userID

        return commandProposedByAUser and commandProposedByAnother 

    def Command_Proposed_By_Another_Collected_A_Yes_Vote(self,reinforcement):

        isAYesVote = reinforcement == 'y'

        commandProposedByAnother = self.Command_Proposed_By_Another()

        return isAYesVote and commandProposedByAnother

    def Command_Proposed_By_Another_Collected_A_Yes_Vote_Achievement_Unlocked(self,username):

        uniqueCommand = self.database.Get_Unique_Command_By_String(self.commandStr)

        initialProposerID = self.database.From_UniqueCommand_Record_Get_UserID(uniqueCommand) 

        initialProposerOfCommand = self.database.Get_User_By_ID(initialProposerID)

        initialProposerName = self.database.From_User_Record_Get_Name(initialProposerOfCommand)

        self.Increment_Users_Pts_Per_Sec(initialProposerOfCommand,initialProposerID)

        msg =       "Achievement unlocked! +" + str(cpg.ptsPerSecIncreaseInterval)

        msg = msg + " XP/sec to " + initialProposerName + " for proposing *" + self.commandStr

        msg = msg + " and getting a win for it from " + username + "." 

        self.print_response("",msg,self.connection)

    def First_Reinforcement_From(self,username):

        reinforcements = self.database.Get_Reinforcements_From(self.userID)

        return len(reinforcements) == 1

        # Their first reinforcement was just stored.

    def First_Reinforcement_From_User_For_This_Robot_Under_This_Command(self,username):

        reinforcements = self.database.Get_Reinforcements_For_Robot_From_User(self.robotID, self.userID)

        matches = 0

        for reinforcement in reinforcements:

            evaluationID = self.database.From_Reinforcement_Record_Get_Evaluation_ID(reinforcement)

            evaluation = self.database.Get_Evaluation_Where_ID_Equals(evaluationID)

            command = self.database.From_Evaluation_Record_Get_Command(evaluation)

            if command == self.commandStr:

                matches = matches + 1

        firstReinforcementFromUser = matches == 1 # Their reinforcement was just stored in the database.

        return firstReinforcementFromUser 

    def First_Reinforcement_Achievement_Unlocked(self,username):

        self.Increment_Users_Pts_Per_Sec(self.user,self.userID)

        msg =       "Achievement unlocked! +" + str(cpg.ptsPerSecIncreaseInterval)
      
        msg = msg + " XP/sec to " + username

        msg = msg + " for speaking to a bot for the first time."

        self.print_response("",msg,self.connection)

    def First_Reinforcement_To_Bot(self,username):

        reinforcements = self.database.Get_Reinforcements_For_Robot(self.robotID)

        return len(reinforcements) == 1 

        # Only one reinforcement for this bot: the one just entered by this user.

    def First_Reinforcement_To_Bot_Achievement_Unlocked(self,username,colorChar):

        self.Increment_Users_Pts_Per_Sec(self.user,self.userID)

        msg =       "Achievement unlocked! +" + str(cpg.ptsPerSecIncreaseInterval)
       
        msg = msg + " XP/sec to " + username 
 
        msg = msg + " for being the first to speak to " + c.colorNameDict[colorChar] + "."

        self.print_response("",msg,self.connection)

    def Handle_Positive_Reinforcement(self,username,color,message):

        self.evaluation = self.database.Get_Evaluation_Where_ID_Equals(self.evaluationID)

        self.commandStr = self.database.From_Evaluation_Record_Get_Command(self.evaluation)

        self.user = self.database.Get_User_By_Name(username)

        self.userID = self.database.From_User_Record_Get_Id(self.user)

        self.user_pays_for(username,cpg.aggressorReinforcementRequest)
        self.database.Add_Reinforcement(self.evaluationID, self.robotID, 'y', username)

    def Handle_Negative_Reinforcement(self,username,message):

        evaluationOfLosingRobot = self.database.Get_Evaluation_That_Occurred_At_The_Same_Time_As(self.evaluationID)

        if not evaluationOfLosingRobot:

            return ''

        evaluationID = self.database.From_Evaluation_Record_Get_Id(evaluationOfLosingRobot)
        robotID      = self.database.From_Evaluation_Record_Get_RobotId(evaluationOfLosingRobot)
        robotColor   = self.database.From_Evaluation_Record_Get_RobotColor(evaluationOfLosingRobot)

        self.database.Add_Reinforcement(evaluationID, robotID, 'n', username)

        return robotColor
 
    def Increment_Users_Pts_Per_Sec(self,user,userID):

        currentPtsPerSec = self.database.From_User_Record_Get_PointsPerSec(user)

        newPtsPerSec = currentPtsPerSec + cpg.ptsPerSecIncreaseInterval

        newPtsPerSec = round(newPtsPerSec,1)

        self.database.Set_PtsPerSec_For_User(newPtsPerSec,userID)

    def Reinforcement_Agrees_With_Crowd_Majority(self,username,reinforcement):

        if not self.First_Reinforcement_From_User_For_This_Robot_Under_This_Command(username):

            return False

        totalYesVotes = self.database.Get_Yes_Votes_For_Robot_Under_Command(self.robotID, self.commandStr)

        totalNoVotes = self.database.Get_No_Votes_For_Robot_Under_Command(self.robotID, self.commandStr)

        totalReinforcementsFromOthers = totalYesVotes + totalNoVotes - 1

        # Subtract one because this user's reinforcement was just stored.

        if totalReinforcementsFromOthers == 0:

            return False

        if reinforcement == 'y':

            totalYesVotes = totalYesVotes - 1 # Subtract the reinforcement just received from the user.

            return totalYesVotes >= totalNoVotes

        else: # reinforcement == 'n'

            totalNoVotes  = totalNoVotes - 1 # Subtract the reinforcement just received from the user.

            return totalNoVotes >= totalYesVotes

    def Reinforcement_Agrees_With_Crowd_Majority_Achievement_Unlocked(self,username):
   
        self.Increment_Users_Pts_Per_Sec(self.user,self.userID)
 
        msg = "Achievement unlocked! +" + str(cpg.ptsPerSecIncreaseInterval) + " XP/sec to " + username + " for agreeing with the crowd."

        self.print_response("",msg,self.connection)

    def reinforcement_response(self, username, reinforcement, color, evaluationID):
        color = c.colorNameDict[color]
        if (reinforcement == 'y'):
            reinforcement_type = "rewarded"
            obeying_or_disobeying = "obeying"
        else:
            reinforcement_type = "scolded"
            obeying_or_disobeying = "disobeying"

        return "{} {} {} for {} !{}" \
               ".".format(username, reinforcement_type, color, obeying_or_disobeying, self.commandStr) 
