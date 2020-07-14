import sqlite3 as lite
import datetime
import os
import sys
import pickle
import time
import numpy
import random

sys.path.insert(0, "..")

from database.word2vecDatabase import Word2VecVectorSpace
import constantsPassiveGame as cpg
import constants as c


class DATABASE:

    def __init__(self, dbFile="database.db", silent_mode=False):
        """
        :param load_large_vector_space: Flag to load in the GoogleNews vector space.
        If false, will load in a much smaller vector space. For testing, use the smaller vector space.
        """
        self.dataDirectory = '../data/'
        self.fileName = self.dataDirectory + dbFile
        self.backupFileName = self.dataDirectory + 'backupDatabase.db'
        self.Connect()
        self.word2vecVectorSpace = Word2VecVectorSpace(database_file='../database/w2vVectorSpace-google.db')
        numpy.set_printoptions(precision=3, threshold=5)

        self.silent_mode = silent_mode
        self.degraded = not self.Is_New_Database()
        if self.degraded and not self.silent_mode:
            warn = DeprecationWarning("You have opened a database using an old command encoding schema. "
                                      "Running in degraded mode: only a few features are supported.")
            print(repr(warn))

        if not self.degraded:
            self.Add_Indices()

    def Active_Users_Present(self):
        """        
        :return: Boolean value indicating whether there any users have typed chat in the last cpg.inactivateUserAfter seconds.
        """
        active_thres = datetime.datetime.now() - datetime.timedelta(seconds=cpg.inactivateUserAfter)

        self.Safe_Execute("SELECT * FROM ChatEntries WHERE date >= ? ", (active_thres,))

        active_usr_id = self.cur.fetchone()

        return active_usr_id != None

    def Is_New_Database(self):
        """
        Checks if Database is pre w2v + leveling system, or post w2v + leveling system.
        :return: True if in format of new database, False otherwise
        """
        exec_string = "PRAGMA table_info(Robots)"
        self.Safe_Execute(exec_string)
        val = self.cur.fetchall()
        names = [tup[1] for tup in val]
        if "DeathDate" not in names:
            return False
        return True

    def Add_Indices(self):
        # evaluation indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS evalId ON Evaluations (Id)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS evalDate ON Evaluations (date)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS evalRobot ON Evaluations (RobotId)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS evalRobot ON Evaluations (RobotColor)")

        # command indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS commandId ON Commands (Id)")

        # chat entries indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS chatEntryUserID ON ChatEntries (UserID)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS chatEntryDate ON ChatEntries (Date)")

        # reinforcements indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS reinforcementId ON Reinforcements (Id)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS reinforcementEvaluationId ON Reinforcements (EvaluationId)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS reinforcementRobotId ON Reinforcements (RobotId)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS reinforcementReinforcement ON Reinforcements (Reinforcement)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS reinforcementDate ON Reinforcements (Date)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS reinforcementUserID ON Reinforcements (UserID)")

        # chat help indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS chatHelpId ON ChatHelp (Id)")

        # robots indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS robotsId ON Robots (Id)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS robotsColorIndex ON Robots (colorIndex)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS robotsAlive ON Robots (alive)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS robotsDeathDate ON Robots (DeathDate)")

        # unique command indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS uniqueCommandsCommand ON UniqueCommands (command)")

        # users indices
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS usersId on Users (Id)")
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS usersName on Users (Name)")

        # speed change request
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS speedChangeId ON SpeedChanges (Id)")

        # show all bots request
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS showAllId ON ShowAllRequests (Id)")

        # show best bot request
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS showBestId ON ShowBestRequests (Id)")

        # buy request
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS buyId ON BuyRequests (Id)")

        # steal request
        self.Safe_Execute("CREATE INDEX IF NOT EXISTS stealId ON StealRequests (Id)")

    def Add_Buy_Request(self, robotID, username):
        """
        :return: None
        """
        ID = self.Get_Next_Available_Buy_Request_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO BuyRequests VALUES (?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        successful = 0
        params = (ID, date, robotID, userID, successful)

        self.Safe_Execute(strng,params)

    def Add_Column(self):

        strng = 'ALTER TABLE Evaluations ADD COLUMN SimulationType INTEGER'

        self.cur.execute(strng)

        self.con.commit()

    def Add_Command(self, command, username):
        """
        :param command: String representation of the command to add to the database.
        :return: None
        """
        # add command to the unique command table. If the command is not new, then increment vote count.
        userID = self.Get_User_ID(username)
        self.Add_Unique_Command(command,userID)

        ID = self.Get_Next_Available_Command_ID()
        strng = 'INSERT INTO Commands VALUES (?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = (ID, command, date, userID)

        self.Safe_Execute(strng, params)
        self.Safe_Execute("UPDATE Users Set CommandCount = CommandCount + 1 WHERE Id = (?)", (userID,))

    def Add_End_Info_Claim_By_Name(self, username):
        executionString = 'UPDATE Users SET EndInfoClaims = 1 WHERE Name = ?'
        params = (str(username),)
        self.Safe_Execute(executionString, params)

    def Add_Environment(self, environmentID):
        """
        :param environmentID: Integer representation of the environment to add to the database.
        :return: None
        """

        strng = 'INSERT INTO Environments VALUES (?,?)'
        locked = 1
        params = (environmentID, locked)

        self.Safe_Execute(strng, params)



    def Add_Help_Message(self, help_message, username):
        """
        :param command: String representation of the help mesage to add to the database.
        :return: None
        """
        ID = self.Get_Next_Available_Help_Message_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO ChatHelp VALUES (?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = (ID, help_message, date, userID)

        self.Safe_Execute(strng, params)


    def Add_Chat_Message(self, entry, username):
        """ Adds every entry entered into database table ChatEntries
        :param entry: String representation of the chat entry to add to the database.
        :return: None
        """
        ID = self.Get_Next_Available_ChatEntries_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO ChatEntries VALUES (?,?,?,?)'
        date = datetime.datetime.now() #.strftime("%Y-%m-%d %H:%M:%S")
        params = (ID, entry, date, userID)

        self.Safe_Execute(strng, params)


    def Add_Evaluation(self, robotID, color, command, speed, environmentID, simulationType):
        ID = self.Get_Next_Available_Evaluation_ID()

        strng = 'INSERT INTO Evaluations VALUES (?,?,?,?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = (str(ID), str(robotID), color, command, date, str(speed), str(environmentID), str(simulationType) )

        self.Safe_Execute(strng, params)



    def Add_Message(self, msg):

        ID = self.Get_Next_Available_Message_ID()

        strng = 'INSERT INTO Messages VALUES (?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        params = (str(ID), msg, date)

        self.Safe_Execute(strng, params)


    def Add_Reinforcement(self, evaluationID, robotID, reinforcement, username):
        reinforcement = reinforcement.lower()
        Id = self.Get_Next_Available_Reinforcement_ID()
        userID = self.Get_User_ID(username)
        digested = 0
        strng = 'INSERT INTO Reinforcements VALUES (?,?,?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = (str(Id), str(evaluationID), str(robotID), reinforcement, date, userID,digested)

        self.Safe_Execute(strng, params)
        if reinforcement == 'y':
            self.Safe_Execute("UPDATE Users Set PosReinforcements = PosReinforcements + 1 WHERE Id = (?)", (userID,))
        elif reinforcement == 'n':
            self.Safe_Execute("UPDATE Users Set NegReinforcements = NegReinforcements + 1 WHERE Id = (?)", (userID,))



    def Add_Dummy_Robot_Data(self, color, parent_id, alive, owner_id):
        id = self.Get_Next_Available_Robot_ID()
        strng = 'INSERT INTO Robots VALUES (?,?,?,?,?,?,?)'
        birth_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        death_date = "9999-01-01 12:00:00"
        params = (str(id), color, parent_id, birth_date, death_date, alive, owner_id)
        self.Safe_Execute(strng, params)


    def Add_Robot(self, robot):
        """
        :param robot:
        :return:
        """
        ID = self.Get_Next_Available_Robot_ID()
        birth_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        death_date = "9999-01-01 12:00:00"
        owner_id = -1
        alive_state = 1
        locked = 1 
        params = (str(ID), str(robot.colorIndex), str(robot.parentID), birth_date, death_date, alive_state, owner_id, locked)

        strng = 'INSERT INTO Robots VALUES (?,?,?,?,?,?,?,?)'

        self.Safe_Execute(strng, params)


        filename = "../data/robot" + str(robot.ID) + ".p"
        pickle.dump(robot, open(filename, "wb"))

    def Add_Show_All_Request(self, username):
        """
        :return: None
        """
        ID = self.Get_Next_Available_Show_All_Request_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO ShowAllRequests VALUES (?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        honored = 0
        params = (ID, date, userID, honored)

        self.Safe_Execute(strng, params)

    def Add_Show_Best_Request(self, username):
        """
        :return: None
        """
        ID = self.Get_Next_Available_Show_Best_Request_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO ShowBestRequests VALUES (?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        honored = 0
        params = (ID, date, userID, honored)

        self.Safe_Execute(strng, params)

    def Add_Speed_Change_Request(self, speedChange, username):
        """
        :param speedChange: String representation of the speed change (+ or -) 
        :return: None
        """
        ID = self.Get_Next_Available_Speed_Change_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO SpeedChanges VALUES (?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        honored = 0
        params = (ID, speedChange, date, userID, honored)

        self.Safe_Execute(strng, params)

    def Add_Start_Info_Claim_By_Name(self, username):
        executionString = 'UPDATE Users SET StartInfoClaims = 1 WHERE Name = ?'
        params = (str(username),)
        self.Safe_Execute(executionString, params)

    def Add_Steal_Request(self, robotID, username):
        """
        :return: None
        """
        ID = self.Get_Next_Available_Steal_Request_ID()
        userID = self.Get_User_ID(username)
        strng = 'INSERT INTO StealRequests VALUES (?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        successful = 0
        params = (ID, date, robotID, userID, successful)

        self.Safe_Execute(strng, params)


    def Add_Unique_Command(self, command, userID):
        """
        This method starts by attempting to get the vector representation of the given command.
        Then, this method pickles the numpy.ndarray to bytes and stores the command in the database.

        :param command: String representation of the command to add. Raises exception if command can not be vectorized.
        :return: None
        """
        if self.Command_Is_New(command):

            try:
                cmd_encoding = self.Get_Command_Vector_Encoding(command)
            except KeyError as e:
                raise e

            raw_cmd_encoding = pickle.dumps(cmd_encoding, protocol=0)

            string = 'INSERT INTO UniqueCommands VALUES (?,?,?,?,?)'
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            votes = 1
            params = (command, raw_cmd_encoding, date, votes, userID)

            self.Safe_Execute(string, params)
    
        else:
            self.Safe_Execute("UPDATE UniqueCommands Set Votes = Votes + 1 WHERE Command = (?)", (command,))

    def Add_User(self, username):
        ID = self.Get_Next_Available_User_ID()
        dateAdded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pos_reinforcement = 0
        neg_reinforcement = 0
        commandCount = 0
        rewardClaims = 0
        params = (ID, username, pos_reinforcement, neg_reinforcement, commandCount, dateAdded, cpg.startingPoints, cpg.startingPtsPerSec, rewardClaims, rewardClaims) 

        self.Safe_Execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        
        print(self.Get_User_By_Name(username))

    def Aggressor_Can_Kill_Defender(self, aggressorID, defenderID):

        [ea, ya, na] = self.Get_Info_For_Robot(aggressorID)
        [ed, yd, nd] = self.Get_Info_For_Robot(defenderID)

        aggressorHasMoreYesVotes = ya > yd

        aggressorHasLessNoVotes = na < nd

        return aggressorHasMoreYesVotes and aggressorHasLessNoVotes

    def Bot_Is_Dead(self, ID):
        executionString = "SELECT * FROM Robots WHERE Id=?"
        params = (str(ID),)

        self.Safe_Execute(executionString, params)
        bot = self.cur.fetchone()

        return (self.From_Robot_Record_Get_Alive_Status(bot) == 0)

    def Color_Of_Bot(self, ID):
        executionString = "SELECT * FROM Robots WHERE Id=?"
        params = (str(ID),)

        self.Safe_Execute(executionString, params)
        bot = self.cur.fetchone()
        clr = self.Get_Robot_Color_Index(bot)

        return c.colorNamesNoParens[clr]

    def Command_Available(self):
        executionString = "SELECT * FROM Commands"
        self.Safe_Execute(executionString)
        commands = self.cur.fetchall()

        return len(commands) > 0

    def Command_Is_New(self, command):
        """
        :param command: The string representation of the command to look for.
        :return: True if the command is new, False otherwise.
        """
        executionString = "SELECT * FROM UniqueCommands WHERE command=?"
        self.Safe_Execute(executionString, (command.rstrip(),))
        result = self.cur.fetchone()

        return (result == None)

    def Connect(self):
        self.con = lite.connect(self.fileName,detect_types=lite.PARSE_DECLTYPES)
        self.cur = self.con.cursor()

    def Create(self):
        self.Create_Tables()

    def Create_Tables(self):
        self.Safe_Execute("CREATE TABLE " + c.databaseTableBuyRequests)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableChatEntries)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableChatHelp)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableChatUniqueCommands)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableCommands)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableEnvironments)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableEvaluations)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableMessages)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableReinforcements)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableRobots)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableShowAllRequests)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableShowBestRequests)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableSpeedChanges)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableStealRequests)
        self.Safe_Execute("CREATE TABLE " + c.databaseTableUsers)

    def Delete_Bad_Commands(self):
        executionString = "Delete from UniqueCommands where Command='what all can i write in this '"
        self.Safe_Execute(executionString)

    def Delete_Command_From_Queue(self):
        executionString = "Delete from Commands where rowid IN (Select rowid from Commands limit 1)"
        self.Safe_Execute(executionString)

    def Delete_Data_Files(self):
        if any(fname.endswith('.p') for fname in os.listdir(self.dataDirectory)):
            os.system("rm " + str(self.dataDirectory) + "*.p")

    def Delete_Evaluation(self, evaluationID):
        executionString = "Delete from Evaluations where Id = ?"
        params = (str(evaluationID),)

        self.Safe_Execute(executionString, params)


    def Delete_Evaluation_If_Non_Reinforced(self, eval):
        raise DeprecationWarning("Please use Delete_Non_Reinforced_Evaluations() instead. It uses 1 call to SQL and is much faster.")

    def Delete_Message(self, messageID):
        executionString = "Delete from Messages where Id = ?"
        params = (str(messageID),)

        self.Safe_Execute(executionString, params)


    def Delete_Non_Reinforced_Evaluations(self, verbose=False, delete_all=False):
        """
        Method to delete some or all non-reinforced evaluations.
        :param verbose: To print or not to print... that is the question. True for printing, False for silent mode.
        :param delete_all: True if want to delete all non-reinforced evals (i.e. prior to data processing). False if only old evals.
        :return: None
        """
        if delete_all:
            delete_thresh = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            delete_thresh = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        if verbose:
            executionString = "SELECT COUNT(*) FROM Evaluations WHERE date <= (?) AND NOT EXISTS (SELECT * FROM Reinforcements WHERE Reinforcements.EvaluationId = Evaluations.Id)"

            self.Safe_Execute(executionString, (delete_thresh, ))
            num_to_del = self.cur.fetchone()

            print("Deleting", num_to_del[0], "nonReinforced evaluations")

        executionString = "DELETE FROM Evaluations WHERE date <= (?) AND NOT EXISTS (SELECT * FROM Reinforcements WHERE Reinforcements.EvaluationId = Evaluations.Id)"

        self.Safe_Execute(executionString, (delete_thresh, ))


    def Delete_Old_And_Non_Reinforced_Evaluations(self):
        raise DeprecationWarning("Please use Delete_Non_Reinforced_Evaluations() instead. It defaults to only deleting old evals")

    def Destroy(self):
        self.Drop_Tables()
        self.Delete_Data_Files()

    def Digest_Reinforcement(self,reinforcementID):

        executionString = "UPDATE Reinforcements SET Digested=1 WHERE Id=?"

        self.Safe_Execute(executionString, (str(reinforcementID),) )

    def Drop_Table(self, tableName):
        if (self.Table_Exists(tableName)):
            self.Safe_Execute("DROP TABLE " + tableName)

    def Drop_Tables(self):

        self.Drop_Table("BuyRequests")
        self.Drop_Table("Commands")
        self.Drop_Table("ChatEntries")
        self.Drop_Table("ChatHelp")
        self.Drop_Table("Environments")
        self.Drop_Table("Evaluations")
        self.Drop_Table("Messages")
        self.Drop_Table("Reinforcements")
        self.Drop_Table("Robots")
        self.Drop_Table("ShowAllRequests")
        self.Drop_Table("ShowBestRequests")
        self.Drop_Table("SpeedChanges")
        self.Drop_Table("StealRequests")
        self.Drop_Table("UniqueCommands")
        self.Drop_Table("Users")

    def Environment_Is_Locked(self, environmentID):

        executionString = "SELECT * FROM Environments WHERE Id=?"
        params = (str(environmentID),)

        self.Safe_Execute(executionString, params)

        environment = self.cur.fetchone()

        locked = int(self.From_Environment_Record_Get_Locked_Status(environment))

        return locked == 1

    def From_Buy_Request_Record_Get_ID(self, buyRequest):

        return int(buyRequest[0])

    def From_Buy_Request_Record_Get_Date(self, buyRequest):

        return buyRequest[1]

    def From_Buy_Request_Record_Get_RobotID(self, buyRequest):
    
        return int(buyRequest[2])

    def From_Buy_Request_Record_Get_UserID(self, buyRequest):

        return int(buyRequest[3])

    def From_Buy_Request_Record_Get_Successful(self, buyRequest):

        return int(buyRequest[4])

    def From_ChatEntries_Record_Get_Id(self, chat):
        return int(chat[0])

    def From_ChatEntries_Record_Get_Entry(self, chat):
        return chat[1]

    def From_ChatEntries_Record_Get_Date(self, chat):
        return chat[2]

    def From_ChatEntries_Record_Get_UserID(self, chat):
        return int(chat[3])

    def From_Environment_Record_Get_ID(self, env):
        return int(env[0])

    def From_Environment_Record_Get_Locked_Status(self, env):
        return int(env[1])

    def From_Evaluation_Record_Get_Id(self, evaluation):
        return int(evaluation[0])

    def From_Evaluation_Record_Get_RobotId(self, evaluation):
        return int(evaluation[1])

    def From_Evaluation_Record_Get_RobotColor(self, evaluation):
        return str(evaluation[2])

    def From_Evaluation_Record_Get_Command(self, evaluation):
        return str(evaluation[3])

    def From_Evaluation_Record_Get_Date(self, evaluation):
        return str(evaluation[4])

    def From_Evaluation_Record_Get_Speed(self, evaluation):
        return int(evaluation[5])

    def From_Evaluation_Record_Get_EnvironmentId(self, evaluation):
        return int(evaluation[6])

    def From_Evaluation_Record_Get_Simulation_Type(self, evaluation):

        if evaluation[7] == None:

            return c.SIMULATE_SURVIVAL
 
        return int(evaluation[7])

    def From_Message_Record_Get_Id(self, message):
        return int(message[0])

    def From_Message_Record_Get_Message(self, message):
        return message[1]

    def From_Message_Record_Get_Date(self, message):
        return str(message[2])

    def From_Reinforcement_Record_Get_ID(self, reinforcement):
        return int(reinforcement[0])

    def From_Reinforcement_Record_Get_Evaluation_ID(self, reinforcement):
        return int(reinforcement[1])

    def From_Reinforcement_Record_Get_Robot_ID(self, reinforcement):
        return int(reinforcement[2])

    def From_Reinforcement_Record_Get_Signal(self, reinforcement):
        return reinforcement[3]

    def From_Reinforcement_Record_Get_Time(self, reinforcement):
        return reinforcement[4]

    def From_Reinforcement_Record_Get_User_ID(self, reinforcement):
        return int(reinforcement[5])

    def From_Reinforcement_Record_Get_Digested(self, reinforcement):
        return int(reinforcement[6])

    def From_Robot_Record_Get_ID(self, robot):
        return int(robot[0])

    def From_Robot_Record_Get_Color_Index(self, robot):
        return int(robot[1])

    def From_Robot_Record_Get_Parent_ID(self, robot):
        return int(robot[2])

    def From_Robot_Record_Get_Creation_Date(self, robot):
        return robot[3]

    def From_Robot_Record_Get_Death_Date(self, robot):
        return robot[4]

    def From_Robot_Record_Get_Alive_Status(self, robot):
        return int(robot[5])

    def From_Robot_Record_Get_Owner_ID(self, robot):
        return int(robot[6])

    def From_Robot_Record_Get_Locked_Status(self, robot):
        return int(robot[7])

    def From_Show_All_Request_Record_Get_ID(self, showAllRequest):

        return int(showAllRequest[0])

    def From_Show_All_Request_Record_Get_Date(self, showAllRequest):

        return showAllRequest[1]

    def From_Show_All_Request_Record_Get_UserID(self, showAllRequest):

        return int(showAllRequest[2])

    def From_Show_All_Request_Record_Get_Honored(self, showAllRequest):

        return int(showAllRequest[3])

    def From_Show_Best_Request_Record_Get_ID(self, showBestRequest):

        return int(showBestRequest[0])

    def From_Show_Best_Request_Record_Get_Date(self, showBestRequest):

        return showBestRequest[1]

    def From_Show_Best_Request_Record_Get_UserID(self, showBestRequest):

        return int(showBestRequest[2])

    def From_Show_Best_Request_Record_Get_Honored(self, showBestRequest):

        return int(showBestRequest[3])

    def From_Speed_Change_Request_Record_Get_ID(self, speedChangeRequest):

        return int(speedChangeRequest[0])

    def From_Speed_Change_Request_Record_Get_Faster_Or_Slower(self, speedChangeRequest):

        return speedChangeRequest[1]

    def From_Speed_Change_Request_Record_Get_Date(self, speedChangeRequest):

        return speedChangeRequest[2]

    def From_Speed_Change_Request_Record_Get_UserID(self, speedChangeRequest):

        return int(speedChangeRequest[3])

    def From_Speed_Change_Request_Record_Get_Honored(self, speedChangeRequest):

        return int(speedChangeRequest[4])

    def From_Steal_Request_Record_Get_ID(self, stealRequest):

        return int(stealRequest[0])

    def From_Steal_Request_Record_Get_Date(self, stealRequest):

        return stealRequest[1]

    def From_Steal_Request_Record_Get_RobotID(self, stealRequest):
   
        return int(stealRequest[2])

    def From_Steal_Request_Record_Get_UserID(self, stealRequest):

        return int(stealRequest[3])

    def From_UniqueCommand_Record_Get_String(self, uniqueCommand):
        return uniqueCommand[0]

    def From_UniqueCommand_Record_Get_CommandEncoding(self, uniqueCommand):
        return uniqueCommand[1]

    def From_UniqueCommand_Record_Get_Date(self, uniqueCommand):
        return uniqueCommand[2]

    def From_UniqueCommand_Record_Get_Votes(self, uniqueCommand):
        return int(uniqueCommand[3])

    def From_UniqueCommand_Record_Get_UserID(self, uniqueCommand):
        return int(uniqueCommand[4])

    def From_User_Record_Get_Id(self,user):
        return int(user[0])

    def From_User_Record_Get_Name(self,user):
        return user[1]

    def From_User_Record_Get_PosReinforcements(self,user):
        return int(user[2])

    def From_User_Record_Get_NegReinforcements(self,user):
        return int(user[3])

    def From_User_Record_Get_CommandCount(self,user):
        return int(user[4])

    def From_User_Record_Get_DateAdded(self,user):
        return user[5]

    def From_User_Record_Get_Points(self,user):
        return float(user[6])

    def From_User_Record_Get_PointsPerSec(self,user):
        return float(user[7])

    def Get_B_Index_For_Robot(self, robotID):
        commands = self.Get_Commands_Robot_Is_Most_Obedient_To(robotID)
        BIndex = 0

        for command in sorted(commands, key=commands.get, reverse=True):
            numYesVotes = commands[command]
            if (numYesVotes > BIndex):
                BIndex = BIndex + 1

        return BIndex

    def Get_B_Index_For_Robot_At_Time(self, robotID, time):
        commands = self.Get_Commands_Robot_Is_Most_Obedient_To_At_Time(robotID, time)
        BIndex = 0

        for command in sorted(commands, key=commands.get, reverse=True):
            numYesVotes = commands[command]
            if (numYesVotes > BIndex):
                BIndex = BIndex + 1

        return BIndex

    def Get_Buy_Requests(self):
        executionString = "SELECT * FROM BuyRequests"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Command_Encoding(self, command):
        """
        Looks for and returns the vector encoding of the given command.

        :param command: The string representation of the command to fetch the encoding format of
        :type command: str
        :return: A N by D numpy array of the vectorized command. N is the number of words sent, corresponding to the number of rows.
                Each row is D elements long. This comes from the dimensionality of the vector space used.
        :rtype: numpy.ndarray
        """
        executionString = "SELECT * FROM UniqueCommands WHERE command = ?"

        params = (command.rstrip(),)

        self.Safe_Execute(executionString, params)
        raw_cmd = self.cur.fetchone()
        if self.degraded:
            return raw_cmd[1]
        if raw_cmd[1] is not None and isinstance(raw_cmd, float):
            warn = DeprecationWarning("You have opened a database using an old command encoding schema. "
                                      "Running in degraded mode: only a few features are supported.")
            print(repr(warn))
            self.degraded = True
            return raw_cmd[1]

        try:
            return pickle.loads(raw_cmd[1])
        except:
            warn = DeprecationWarning(
                "You have opened a database containing an unsupported command encoding schema. "
                "Running in degraded mode: only reading is supported.")
            print(repr(warn))
            self.degraded = True
            return raw_cmd


    def Get_Command_From_Queue(self):
        executionString = "SELECT * FROM Commands ORDER BY ROWID ASC LIMIT 1"
        self.Safe_Execute(executionString)
        row = self.cur.fetchone()
        command = row[1]

        return command

    def Get_Command_Vector_Encoding(self, command):
        """
        Looks in the vector space for the given command and returns it's assoicated vector if found.
        If no vector exists for the given command, raises a KeyError exception

        :param command: The string encoding of the command to search for.
        :type command: str
        :return: A N by D numpy array of the vectorized command. N is the number of words sent, corresponding to the number of rows.
                Each row is D elements long. This comes from the dimensionality of the vector space used.
        :rtype: numpy.ndarray
        """
        cmds = command.split()
        cmd_encoding = numpy.zeros((len(cmds), len(self.word2vecVectorSpace.get_vector(cmds[0]))))

        for i, cmd in enumerate(cmds):
            cmd_encoding[i] = self.word2vecVectorSpace.get_vector(cmd)
        return cmd_encoding

    def Get_Commands(self):
        executionString = "SELECT * FROM Commands"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Chat_Entered_Since(self,date):

        self.Safe_Execute("SELECT * FROM ChatEntries WHERE Date >= ?", (date,))
        return self.cur.fetchall()

    def Get_Chat_Entries(self):
        executionString = "SELECT * FROM ChatEntries"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Color_Index_And_Highest_B_Index_Among_Living_Robots(self):

        bIndex = -1

        robots = self.Get_Living_Robots()

        for robot in robots:

            robotID = self.From_Robot_Record_Get_ID(robot)
                                   
            currentBIndex = self.Get_B_Index_For_Robot(robotID)

            if currentBIndex > bIndex:

                bIndex = currentBIndex

                colorIndex = self.From_Robot_Record_Get_Color_Index(robot)

        return colorIndex,bIndex

    def Get_Commands_Robot_Is_Most_Obedient_To(self, robotID):
        commands = {}
        uniqueCommands = self.Get_Unique_Commands()

        for uniqueCommand in uniqueCommands:
            commandString = self.From_UniqueCommand_Record_Get_String(uniqueCommand)
            commands[commandString] = 0

        reinforcements = self.Get_Positive_Reinforcements_For_Robot(robotID)

        for reinforcement in reinforcements:
            evaluationID = self.From_Reinforcement_Record_Get_Evaluation_ID(reinforcement)
            evaluation = self.Get_Evaluation_Where_ID_Equals(evaluationID)
            command = self.From_Evaluation_Record_Get_Command(evaluation)
            commands[command] = commands[command] + 1

        return commands

    def Get_Commands_Robot_Is_Most_Obedient_To_At_Time(self, robotID, time):
        commands = {}
        uniqueCommands = self.Get_Unique_Commands()

        for uniqueCommand in uniqueCommands:
            commandString = self.From_UniqueCommand_Record_Get_String(uniqueCommand)
            commands[commandString] = 0

        reinforcements = self.Get_Positive_Reinforcements_For_Robot_At_Time(robotID, time)

        for reinforcement in reinforcements:
            evaluationID = self.From_Reinforcement_Record_Get_Evaluation_ID(reinforcement)
            evaluation = self.Get_Evaluation_Where_ID_Equals(evaluationID)
            command = self.From_Evaluation_Record_Get_Command(evaluation)
            commands[command] = commands[command] + 1

        return commands

    def Get_Current_Evaluation(self):
        executionString = "SELECT * FROM Evaluations ORDER BY date DESC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Get_Dead_Robots_Since(self, date):
        self.Safe_Execute("SELECT * FROM Robots WHERE alive = 0 AND DeathDate >= ?", (date,))
        return self.cur.fetchall()

    def Get_Environment(self, ID):

        executionString = "SELECT * FROM Environments WHERE Id = " + str(ID)
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Environments(self):
        executionString = "SELECT * FROM Environments"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Evaluation_ID(self, evaluation):
        return int(evaluation[0])

    def Get_Evaluation_Where_ID_Equals(self, ID):
        executionString = "SELECT * FROM Evaluations WHERE Id= ?"
        params = (str(ID),)

        self.Safe_Execute(executionString, params)
        return self.cur.fetchone()

    def Get_Evaluation_That_Occurred_At_The_Same_Time_As(self,evaluationID):

        executionString = "SELECT * FROM Evaluations WHERE Id= ?"
        params = (str(evaluationID),)

        self.Safe_Execute(executionString, params)

        evaluation = self.cur.fetchone()

        date = self.From_Evaluation_Record_Get_Date(evaluation)

        evaluationsAtThatTime = self.Get_Evaluations_Where_Date_Equals(date)
        
        if len(evaluationsAtThatTime) != 2:

            return None

        firstEvaluation = evaluationsAtThatTime[0]

        secondEvaluation = evaluationsAtThatTime[1]

        if firstEvaluation == evaluation:

            return secondEvaluation
        else:
            return firstEvaluation

    def Get_Evaluations(self):
        executionString = "SELECT * FROM Evaluations"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Evaluations_Where_Date_Equals(self, date):
        executionString = "SELECT * FROM Evaluations WHERE Date= ?"
        params = (str(date),)
        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Evaluations_Where_RobotID_Equals(self, robotID):
        executionString = "SELECT * FROM Evaluations WHERE RobotId= ?"
        params = (str(robotID),)
        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_First_Reinforcement(self):
        executionString = "SELECT * FROM Reinforcements ORDER BY date LIMIT 1"
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_First_Robot(self):
        executionString = "SELECT * FROM Robots ORDER BY date LIMIT 1"
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Info_For_Robot(self, ID):
        e = self.Get_Robot_Num_Reinforced_Evaluations(ID)
        y = self.Get_Robot_Num_Yeses(ID)
        n = self.Get_Robot_Num_Nos(ID)

        return e, y, n

    def Get_Last_Two_Evaluations(self):
        executionString = "SELECT * FROM Evaluations ORDER BY date DESC LIMIT 2"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Living_Robot_At_Position(self, robotPosition):

        executionString = "SELECT * FROM Robots WHERE alive=1 AND colorIndex=?"
        params = (str(robotPosition),)

        self.Safe_Execute(executionString, params)
        return self.cur.fetchone()

    def Get_Living_Robot_Of_Color(self,colorChar):

        executionString = "SELECT * FROM Robots WHERE alive=1 AND colorIndex = " + str(c.colors.index(colorChar))
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Living_Robots(self):
        executionString = "SELECT * FROM Robots WHERE alive=1"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Locked_Environments(self):
        executionString = "SELECT * FROM Environments WHERE Locked=1"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Locked_Robots(self):
        executionString = "SELECT * FROM Robots WHERE alive=1 AND Locked=1"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Messages(self):
        executionString = "SELECT * FROM Messages"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Most_Recent_Buy_Request(self):
        executionString = "SELECT * FROM BuyRequests ORDER BY date DESC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Get_Most_Recent_Chat_From_User(self,userID):
        executionString = "SELECT * FROM ChatEntries WHERE UserID=? ORDER BY date DESC LIMIT 1"
        params = (userID,)
        self.Safe_Execute(executionString, params)
        return self.cur.fetchone()

    def Get_Most_Recent_Evaluation_With_Bot_Color(self, c):
        executionString = "SELECT Id, RobotId FROM Evaluations WHERE RobotColor=? ORDER BY date DESC LIMIT 1"
        params = (c,)
        self.Safe_Execute(executionString, params)
        bot = self.cur.fetchone()

        if not bot:
            return -1, -1
        else:
            evaluationID = int(bot[0])
            robotID = int(bot[1])
            return evaluationID, robotID

    def Get_Most_Recent_Steal_Request(self):
        executionString = "SELECT * FROM StealRequests ORDER BY date DESC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Get_Most_Recently_Negatively_Reinforced_Bot(self):
        executionString = "SELECT RobotId FROM Reinforcements WHERE Reinforcement='n' ORDER BY date DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return -1
        else:
            return int(ID[0])

    def Get_Newest_Pair_Of_Undigested_Reinforcements(self):

        executionString = "SELECT * FROM Reinforcements WHERE Digested=0 ORDER BY Id DESC LIMIT 2"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Next_Available_Buy_Request_ID(self):
        executionString = "SELECT Id FROM BuyRequests ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Command_ID(self):
        executionString = "SELECT Id FROM Commands ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Evaluation_ID(self):
        executionString = "SELECT Id FROM Evaluations ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Message_ID(self):
        executionString = "SELECT Id FROM Messages ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Help_Message_ID(self):
        executionString = "SELECT Id FROM ChatHelp ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_ChatEntries_ID(self):
        executionString = "SELECT Id FROM ChatEntries ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Reinforcement_ID(self):
        executionString = "SELECT Id FROM Reinforcements ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Robot_ID(self):
        executionString = "SELECT Id FROM Robots ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Show_All_Request_ID(self):
        executionString = "SELECT Id FROM ShowAllRequests ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Show_Best_Request_ID(self):
        executionString = "SELECT Id FROM ShowBestRequests ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Speed_Change_ID(self):
        executionString = "SELECT Id FROM SpeedChanges ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_Steal_Request_ID(self):
        executionString = "SELECT Id FROM StealRequests ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_Next_Available_User_ID(self):

        executionString = "SELECT Id FROM Users ORDER BY Id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        ID = self.cur.fetchone()

        if not ID:
            return 0
        else:
            return int(ID[0]) + 1

    def Get_No_Votes_For_Evaluation(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE EvaluationId=? AND Reinforcement = 'n'"
        params = (str(ID),)

        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Nth_Command_Obeyed_By_Robot(self, n, robotID):

        commands = self.Get_Commands_Robot_Is_Most_Obedient_To(robotID)
     
        sortedCommands = sorted(commands, key=commands.get, reverse=True)

        return sortedCommands[n]

    def Get_Num_Undigested_Reinforcements(self):

        executionString = "SELECT * FROM Reinforcements WHERE Digested=0"
        self.Safe_Execute(executionString)
        return len(self.cur.fetchall())

    def Get_Number_Of_Queued_Messages(self):

        executionString = "SELECT * FROM Messages"
        self.Safe_Execute(executionString)
        return len(self.cur.fetchall())

    def Get_Oldest_Pair_Of_Undigested_Reinforcements(self):

        executionString = "SELECT * FROM Reinforcements WHERE Digested=0 ORDER BY Id ASC LIMIT 2"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Oldest_Unprocessed_Message(self):

        executionString = "SELECT * FROM Messages ORDER BY Id ASC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Get_Original_Robots(self):
        executionString = "SELECT * FROM Robots ORDER BY Id LIMIT ?"
        params = (str(c.popSize),)

        self.Safe_Execute(executionString, params)
        return self.cur.fetchall()

    def Get_Positive_Reinforcements_For_Robot(self, robotID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId = ? AND Reinforcement='y'"
        params = (str(robotID),)
        self.Safe_Execute(executionString, params)
        yesVotes = self.cur.fetchall()
        return yesVotes

    def Get_Positive_Reinforcements_For_Robot_At_Time(self, robotID, time):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId = ? AND Reinforcement='y' AND date <= datetime(?) "
        params = (str(robotID), time)
        self.Safe_Execute(executionString, params)

        yesVotes = self.cur.fetchall()
        return yesVotes

    def Get_Reinforcement(self, reinforcement):
        return reinforcement[3]

    def Get_Reinforcements(self):
        executionString = "SELECT * FROM Reinforcements"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Reinforcements_For_Robot(self, robotID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId = ?"
        params = (str(robotID),)
        self.Safe_Execute(executionString, params)
        return self.cur.fetchall()

    def Get_Show_All_Request(self):
        executionString = "SELECT * FROM ShowAllRequests WHERE Honored=0 ORDER BY ROWID ASC LIMIT 1"
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Show_All_Requests(self):
        executionString = "SELECT * FROM ShowAllRequests"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Show_Best_Request(self):
        executionString = "SELECT * FROM ShowBestRequests WHERE Honored=0 ORDER BY ROWID ASC LIMIT 1"
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Show_Best_Requests(self):
        executionString = "SELECT * FROM ShowBestRequests"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Speed_Changes(self):
        executionString = "SELECT * FROM SpeedChanges"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Speed_Change_Request(self):
        executionString = "SELECT * FROM SpeedChanges WHERE Honored=0 ORDER BY ROWID ASC LIMIT 1"
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Steal_Requests(self):
        executionString = "SELECT * FROM StealRequests"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Help_Messages(self):
        executionString = "SELECT * FROM ChatHelp"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Live_Robots(self):

        executionString = "SELECT * FROM Robots WHERE alive=1"

        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Reinforcements_For_Evaluation(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE EvaluationId=?"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Reinforcements_For_Robot(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId=?"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Reinforcements_For_Robot_From_User(self, RobotId, UserId):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId=? AND UserId=?"
        params = (RobotId, UserId)
        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Reinforcements_From(self, UserId):
        executionString = "SELECT * FROM Reinforcements WHERE UserId=?"
        params = (str(UserId),)
        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Reproduction_Chance_For_Robot(self, ID):
        [e, y, n] = self.Get_Info_For_Robot(ID)
        executionString = "SELECT * FROM Robots WHERE alive=1"
        self.Safe_Execute(executionString)
        bots = self.cur.fetchall()
        numberOfWins = 0
        numberOfOthers = 0

        for bot in bots:
            otherID = self.Get_Robot_ID(bot)
            if (otherID != ID):
                [eo, yo, no] = self.Get_Info_For_Robot(otherID)
                numberOfWins = numberOfWins + self.Beat_Other_Bot(e, y, n, eo, yo, no)
                numberOfOthers = numberOfOthers + 1

        probOfReproducing = float(numberOfWins) / float(numberOfOthers)
        chanceOfReproducing = probOfReproducing * 100

        return (chanceOfReproducing)

    def Get_Robot_By_ID(self, ID):

        executionString = "SELECT * FROM Robots WHERE Id = " + str(ID)
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Robot_Num_Evaluations(self, ID):
        executionString = "SELECT * FROM Evaluations WHERE RobotId=?"
        params = (str(ID),)

        self.Safe_Execute(executionString, params)

        return len(self.cur.fetchall())

    def Get_Robot_Num_Reinforced_Evaluations(self, ID):
        executionString = "SELECT DISTINCT EvaluationId FROM Reinforcements WHERE RobotId=?"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)

        return len(self.cur.fetchall())

    def Get_Robot_Num_Digested_Nos(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId=? AND Digested=1"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)
        n = 0

        for r in self.cur.fetchall():
            if (self.Get_Reinforcement(r) == 'n'):
                n = n + 1

        return n

    def Get_Robot_Num_Digested_Yeses(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId=? AND Digested=1"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)
        y = 0

        for r in self.cur.fetchall():
            if (self.Get_Reinforcement(r) == 'y'):
                y = y + 1

        return y

    def Get_Robot_Num_Yeses(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId=?"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)
        y = 0

        for r in self.cur.fetchall():
            if self.Get_Reinforcement(r) == 'y':
                y = y + 1

        return y

    def Get_Robot_Num_Nos(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId=?"
        params = (str(ID),)
        self.Safe_Execute(executionString, params)
        n = 0

        for r in self.cur.fetchall():
            if self.Get_Reinforcement(r) == 'n':
                n = n + 1

        return n

    def Get_Robot_Of_Color(self,colorChar):

        executionString = "SELECT * FROM Robots WHERE colorIndex = " + str(c.colors.index(colorChar))
        self.Safe_Execute(executionString)

        return self.cur.fetchone()

    def Get_Robots(self):
        executionString = "SELECT * FROM Robots"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Robots_Owned_By(self,userID):
        executionString = "SELECT * FROM Robots WHERE OwnerID = ?"
        self.Safe_Execute(executionString, (userID,))

        return self.cur.fetchall()

    def Get_Unique_Command_By_String(self, commandStr):
        executionString = "SELECT * FROM UniqueCommands WHERE Command = ?"
        self.Safe_Execute(executionString, (commandStr,))
        return self.cur.fetchone()

    def Get_Unique_Commands_Votes(self):
        """
        :return: An array of tuples. Each tuple contains the command string and the number of votes it has recieved.
        """

        executionString = "SELECT Command, Votes FROM UniqueCommands;"
        self.Safe_Execute(executionString)
        cmds = self.cur.fetchall()
        return list(sorted(cmds, key=lambda x: x[1], reverse=True));

    def Get_Unique_Commands(self):
        """
        :return: An array of tuples. Each tuple contains the command string, the vector encoded form, and a timestamp.
        Note that the database internally stores the vector arrays in the pickle format and converts them to arrays on read.
        """
        executionString = "SELECT * FROM UniqueCommands"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Unlocked_Environments(self):
        executionString = "SELECT * FROM Environments WHERE Locked=0"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_Unlocked_Robots(self):
        executionString = "SELECT * FROM Robots WHERE alive=1 AND Locked=0"
        self.Safe_Execute(executionString)
        return self.cur.fetchall()

    def Get_User_By_ID(self, user_id):
        executionString = "SELECT * FROM Users WHERE Id = ?"
        self.Safe_Execute(executionString, (int(user_id),))
        return self.cur.fetchone()

    def Get_User_By_Name(self, user_name):
        executionString = "SELECT * FROM Users WHERE Name = ?"
        self.Safe_Execute(executionString, (user_name,))
        return self.cur.fetchone()

    def Get_User_Stats(self, username):
        """
        gets and returns all stats for a given user.
        :param username:
        :return:
        """
        executionString = "SELECT * FROM Users WHERE Name = ?"
        self.Safe_Execute(executionString, (username, ))
        return self.cur.fetchone()

    def Get_User_ID(self, username):
        """
        :param username: A string
        :return: An integer, the Id of the user corresponding to the username param
        """
        executionString = "SELECT Id FROM Users WHERE Name='" + username + "'"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()[0]

    def Get_User_Points(self, username):
        """
        :param username: A string
        :return: A real, the corresponding user's current points.
        """
        executionString = "SELECT Points FROM Users WHERE Name='" + username + "'"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()[0]

    def Set_Buy_Request_Successful_By_ID(self,requestID):

        executionString = "UPDATE BuyRequests SET Successful=1 WHERE Id=?"
        self.Safe_Execute(executionString, (str(requestID),) )


    def Set_Owner_Of_Robot(self,userID,robotID):

        executionString = "UPDATE Robots SET OwnerID=? WHERE Id=?"
        self.Safe_Execute(executionString, (str(userID),str(robotID)) )


    def Set_Points_For_User_By_ID(self,points,userID):

        executionString = "UPDATE Users SET Points= ? WHERE Id=?"
        self.Safe_Execute(executionString, (points, userID))

    def Set_Points_For_User_By_Name(self,points,username):

        executionString = "UPDATE Users SET Points= ? WHERE Name=?"
        self.Safe_Execute(executionString, (points, username))


    def Set_PtsPerSec_For_User(self,ptsPerSec,userID):

        executionString = "UPDATE Users SET PointsPerSec=? WHERE Id=?"
        self.Safe_Execute(executionString, (str(ptsPerSec),str(userID)) )


    def Set_Show_All_Request_Honored(self,requestID):

        executionString = "UPDATE ShowAllRequests SET Honored=1 WHERE Id=?"
        self.Safe_Execute(executionString, (str(requestID),) )

    def Set_Show_Best_Request_Honored(self,requestID):

        executionString = "UPDATE ShowBestRequests SET Honored=1 WHERE Id=?"
        self.Safe_Execute(executionString, (str(requestID),) )

    def Set_Speed_Change_Request_Honored(self,speedChangeID):

        executionString = "UPDATE SpeedChanges SET Honored=1 WHERE Id=?"
        self.Safe_Execute(executionString, (str(speedChangeID),) )


    def Set_Steal_Request_Successful_By_ID(self,requestID):

        executionString = "UPDATE StealRequests SET Successful=1 WHERE Id=?"
        self.Safe_Execute(executionString, (str(requestID),) )


    def Get_Lowest_Numbered_Locked_Environment(self):

        executionString = "SELECT * FROM Environments WHERE locked=1 ORDER BY id ASC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Get_Num_Entries_By_User_In_Table(self, username, tablename):
        """
        :param username:
        :param tablename: should be either "Commands", "Reinforcements", "ChatHelp", "ChatEntries"
        :return: number of entries of type tablename
        """
        UserID = self.Get_User_ID(username)
        executionString = "SELECT * FROM " + tablename + " WHERE UserID='" + str(UserID) + "'"
        self.Safe_Execute(executionString)
        return len(self.cur.fetchall())

    def Get_Users(self):
        executionString = "SELECT * FROM Users"
        self.Safe_Execute(executionString)

        return self.cur.fetchall()

    def Get_Yes_Votes_For_Evaluation(self, ID):
        executionString = "SELECT * FROM Reinforcements WHERE EvaluationId = ? AND Reinforcement = 'y'"
        params = (str(ID),)

        self.Safe_Execute(executionString, params)

        return self.cur.fetchall()

    def Get_Yes_Votes_For_Robot_Under_Command(self, robotID, commandString):
        executionString = "SELECT * FROM Evaluations WHERE RobotId = ? AND command = ?"
        params = (str(robotID), commandString.rstrip())

        self.Safe_Execute(executionString, params)
        evaluations = self.cur.fetchall()

        yesVotes = 0

        for evaluation in evaluations:
            evaluationID = self.From_Evaluation_Record_Get_Id(evaluation)
            reinforcements = self.Get_Yes_Votes_For_Evaluation(evaluationID)
            yesVotes = yesVotes + len(reinforcements)

        return yesVotes

    def Get_No_Votes_For_Robot_Under_Command(self,robotID,commandString):
        executionString = "SELECT * FROM Evaluations WHERE RobotId = " + str(robotID) + " AND command = '" + commandString.rstrip() + "'" 
        self.Safe_Execute(executionString)
        evaluations = self.cur.fetchall()

        noVotes = 0

        for evaluation in evaluations:

            evaluationID = self.From_Evaluation_Record_Get_Id(evaluation) 

            reinforcements = self.Get_No_Votes_For_Evaluation(evaluationID)

            noVotes = noVotes + len(reinforcements)

        return noVotes

    def Get_Youngest_Bot_Of_ColorIndex(self,colorIndex):

        executionString = "SELECT * FROM Robots WHERE colorIndex=" + str(colorIndex) + " ORDER BY id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Get_Youngest_Locked_Bot(self):

        executionString = "SELECT * FROM Robots WHERE alive=1 AND locked=1 ORDER BY id DESC LIMIT 1"
        self.Safe_Execute(executionString)
        return self.cur.fetchone()

    def Kill_Bot(self, ID):
        death_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        strng = 'UPDATE Robots SET alive = 0, DeathDate = ? WHERE Id = ?'
        params = (death_date, ID)

        self.Safe_Execute(strng, params)


    def Lock_Bot(self, ID):

        strng = 'UPDATE Robots SET locked = 1 WHERE Id = ?'
        params = (ID,)

        self.Safe_Execute(strng, params)


    def Lock_Environment(self, ID):

        strng = 'UPDATE Environments SET Locked = 1 WHERE Id = ?'
        params = (ID,)

        self.Safe_Execute(strng, params)


    def New_User(self, username):
        executionString = "SELECT * FROM Users WHERE Name = ?"
        params = (str(username),)

        self.Safe_Execute(executionString, params)
        user = self.cur.fetchone()

        return (user is None)

    def No_Negative_Reinforcements(self):
        executionString = "SELECT * FROM Reinforcements WHERE Reinforcement = 'n' "
        self.Safe_Execute(executionString)

        return (self.cur.fetchone() is None)

    def Num_Unprocessed_Messages(self):

        executionString = "SELECT * FROM Messages"
        self.Safe_Execute(executionString)

        return len( self.cur.fetchall() )

    def Populate(self):
        """
        This method populates the database with a three sample entries for each table.
        I think it is less horrible now.
        """
        # Add users
        self.Add_User("Caesar")
        self.Add_User("Annie")
        self.Add_User("Bill")
        # Add commands
        self.Add_Command("walk", "Bill")
        self.Add_Command("run", "Caesar")
        self.Add_Command("jump", "Annie")
        # Add evaluations
        self.Add_Evaluation(0, "r", "walk")
        self.Add_Evaluation(1, "y", "run")
        self.Add_Evaluation(2, "g", "jump")
        # Add reinforcements
        self.Add_Reinforcement(0, 0, "y", "Bill")
        self.Add_Reinforcement(1, 1, "n", "Annie")
        self.Add_Reinforcement(2, 2, "y", "Annie")
        self.Add_Reinforcement(2, 2, "y", "Caesar")
        # Add three sample robots for testing
        self.Add_Dummy_Robot_Data(0, 0, 1, 0)
        self.Add_Dummy_Robot_Data(1, 0, 1, 1)
        self.Add_Dummy_Robot_Data(2, 1, 0, 2)

    def Print(self):
        self.Print_Buy_Requests()
        self.Print_Chat_Entries()
        self.Print_Commands()
        self.Print_Environments()
        self.Print_Evaluations()
        self.Print_Help_Messages()
        self.Print_Messages()
        self.Print_Reinforcements()
        self.Print_Robots()
        self.Print_Show_All_Requests()
        self.Print_Show_Best_Requests()
        self.Print_Speed_Changes()
        self.Print_Steal_Requests()
        self.Print_Unique_Commands()
        self.Print_Users()

    def Print_Buy_Requests(self):
        print(c.databaseTableBuyRequests)
        buyRequests = self.Get_Buy_Requests()

        for buyRequest in buyRequests:
            print(buyRequest)

        print('')

    def Print_Commands(self):
        print(c.databaseTableCommands)
        commands = self.Get_Commands()

        for command in commands:
            print(command)

        print('')

    def Print_Environments(self):

        print(c.databaseTableEnvironments)
        environments = self.Get_Environments()

        for environment in environments:
            print(environment)

        print('')

    def Print_Evaluations(self):
        print(c.databaseTableEvaluations)
        evaluations = self.Get_Evaluations()

        for evaluation in evaluations:
            print(evaluation)

        print('')

    def Print_Help_Messages(self):
        print(c.databaseTableChatHelp)
        helpMessages = self.Get_Help_Messages()

        for helpMessage in helpMessages:
            print(helpMessage)

        print('')

    def Print_Messages(self):
        print(c.databaseTableMessages)
        messages = self.Get_Messages()

        for message in messages:
            print(message)

        print('')

    def Print_Chat_Entries(self):
        print(c.databaseTableChatEntries)
        entries = self.Get_Chat_Entries()

        for entry in entries:
            print(entry)

        print('')

    def Print_Reinforcements(self):
        print(c.databaseTableReinforcements)
        reinforcements = self.Get_Reinforcements()

        for reinforcement in reinforcements:
            print(reinforcement)

        print('')

    def Print_Robots(self):
        print(c.databaseTableRobots)
        robots = self.Get_Robots()

        for robot in robots:
            print(robot)

        print('')

    def Print_Show_All_Requests(self):
        print(c.databaseTableShowAllRequests)
        showAllRequests = self.Get_Show_All_Requests()

        for showAllRequest in showAllRequests:
            print(showAllRequest)

        print('')

    def Print_Show_Best_Requests(self):
        print(c.databaseTableShowBestRequests)
        showBestRequests = self.Get_Show_Best_Requests()

        for showBestRequest in showBestRequests:
            print(showBestRequest)

        print('')

    def Print_Speed_Changes(self):
        print(c.databaseTableSpeedChanges)
        speedChangeRequests = self.Get_Speed_Changes()

        for speedChangeRequest in speedChangeRequests:
            print(speedChangeRequest)

        print('')

    def Print_Steal_Requests(self):
        print(c.databaseTableStealRequests)
        stealRequests = self.Get_Steal_Requests()

        for stealRequest in stealRequests:
            print(stealRequest)

        print('')

    def Print_Unique_Commands(self):
        print(c.databaseTableChatUniqueCommands)
        uniqueCommands = self.Get_Unique_Commands()
        for uniqueCommand in uniqueCommands:
            print(uniqueCommand[0],"[word2vec vec]",uniqueCommand[2],uniqueCommand[3],uniqueCommand[4])
            # print(uniqueCommand)

        print('')

    def Print_Users(self):
        print(c.databaseTableUsers)
        users = self.Get_Users()

        for user in users:
            print(user)

        print('')

    def Push_To_Dropbox(self):
        moveToBackup = "mv " + str(self.fileName) + " " + str(self.backupFileName)
        os.system(moveToBackup)
        moveBackToPrimary = "mv " + str(self.backupFileName) + " " + str(self.fileName)
        os.system(moveBackToPrimary)

    def Robot_Is_Alive(self, robotID):

        executionString = "SELECT * FROM Robots WHERE Id=?"
        params = (str(robotID),)

        self.Safe_Execute(executionString, params)

        robot = self.cur.fetchone()

        alive = int(self.From_Robot_Record_Get_Alive_Status(robot))

        return alive == 1

    def Robot_Is_Locked(self, robotID):

        executionString = "SELECT * FROM Robots WHERE Id=?"
        params = (str(robotID),)

        self.Safe_Execute(executionString, params)

        robot = self.cur.fetchone()

        if not robot:
 
            return -1

        locked = int(self.From_Robot_Record_Get_Locked_Status(robot))

        return locked == 1

    def Robot_With_This_Color_Index_Is_Locked(self, robotColorIndex):

        executionString = "SELECT * FROM Robots WHERE colorIndex=? AND alive=1"
        params = (str(robotColorIndex),)

        self.Safe_Execute(executionString, params)

        robot = self.cur.fetchone()

        locked = int(self.From_Robot_Record_Get_Locked_Status(robot))

        return locked == 1

    def Robot_Shown_Recently(self, robotID):

        executionString = "SELECT * FROM Evaluations ORDER BY id DESC LIMIT 4"
        self.Safe_Execute(executionString)
        mostRecentFourEvaluations = self.cur.fetchall()

        robotShownRecently = False

        for recentEvaluation in mostRecentFourEvaluations:

            recentRobotID = self.From_Evaluation_Record_Get_RobotId(recentEvaluation)

            if robotID == recentRobotID:
                robotShownRecently = True

        return robotShownRecently

    def Remove_Dead_Bots(self):
        executionString = "DELETE FROM Robots WHERE alive=0"
        self.Safe_Execute(executionString)

    def Reset(self):
        self.Destroy()
        self.Create()

    def Robots_Table_Is_Empty(self):

        executionString = "SELECT * FROM Robots"
        self.Safe_Execute(executionString)

        return self.cur.fetchall() == None

    def Safe_Execute(self,*args):

        for i in range(100):

            try:
                self.cur.execute(*args)
            except:
                time.sleep( random.uniform(0.01,0.05) )
            else:
                break

        for i in range(100):

            try:
                self.con.commit()
            except:
                time.sleep( random.uniform(0.01,0.05) )
            else:
                break

    def Table_Exists(self, tableName):
        executionString = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        params = (tableName,)
        self.Safe_Execute(executionString, params)
        result = self.cur.fetchone()

        return (result != None)

    def Total_Evaluations(self):
        executionString = "SELECT * FROM Evaluations"
        self.Safe_Execute(executionString)
        bots = self.cur.fetchall()

        return len(bots)

    def Total_Negative_Reinforcements(self):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId > -1 AND Reinforcement='n' "
        self.Safe_Execute(executionString)
        noVotes = self.cur.fetchall()

        return len(noVotes)

    def Total_Positive_Reinforcements(self):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId > -1 AND Reinforcement='y' "
        self.Safe_Execute(executionString)
        yesVotes = self.cur.fetchall()

        return len(yesVotes)

    def Total_Reinforcements(self):
        executionString = "SELECT * FROM Reinforcements WHERE RobotId > -1"
        self.Safe_Execute(executionString)
        reinforcements = self.cur.fetchall()

        return len(reinforcements)

    def Total_Robots(self):
        executionString = "SELECT * FROM Robots"
        self.Safe_Execute(executionString)
        bots = self.cur.fetchall()

        return len(bots)

    def Total_Users(self):
        executionString = "SELECT * FROM Users"
        self.Safe_Execute(executionString)
        users = self.cur.fetchall()

        return len(users)

    def Try_Get_Command_Vector_Encoding(self, command):
        """
        Checks to see if there is a vector in the vector space for the given command

        :param command: The command to look for
        :type command: str
        :return: True if the command is found in the vector space, False otherwise
        :rtype: tuple of (fully valid, unrecognized cmds). If not fully valid, returns false with a list of the commands
        not found in our vocabulary.
        """
        cmds = command.split()
        unrecognized_cmd_parts = []
        for cmd in cmds:
            try:
                self.Get_Command_Vector_Encoding(cmd)
            except:
                unrecognized_cmd_parts.append(cmd)
        if unrecognized_cmd_parts == []:
            return (True, unrecognized_cmd_parts)
        else:
            return (False, unrecognized_cmd_parts)

    def Unlock_Bot(self, ID):

        strng = 'UPDATE Robots SET locked = 0 WHERE Id = ?'
        params = (ID,)

        self.Safe_Execute(strng, params)


    def Unlock_Environment(self, ID):

        strng = 'UPDATE Environments SET Locked = 0 WHERE Id = ?'
        params = (ID,)

        self.Safe_Execute(strng, params)


    def User_Exists(self, username):
        executionString = "SELECT * FROM Users WHERE Name=?"
        params = (username,)
        self.Safe_Execute(executionString, params)
        users = self.cur.fetchall()

        return len(users) > 0
