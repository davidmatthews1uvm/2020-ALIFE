import constants as c
import random

class COMMAND:

    def __init__(self, database, distribution="uniform"):

        self.database = database

        if self.No_Commands_Available_In_Database():

                self.Add_Default_Commands_To_Database()

        if self.database.Command_Available():

            self.Set_Command_Issued_By_User()

        else:
            if distribution == "uniform":
                self.Set_Valid_Random_Command()
            elif distribution == "ranked":
                self.Set_Valid_Random_Command(ranked=True)
            else:
                raise ValueError("COMMAND object can not understand the option distribution=" + str(distribution))

    def Get_Encoding(self):

        return self.database.Get_Command_Encoding(self.command) 

    def Get_String(self):

        return self.command

    def Set_String(self,commandString):

        self.command = commandString

# --------------- Private methods -----------------------

    def Add_Default_Commands_To_Database(self):

        for defaultCommand in c.defaultCommands:

            print(defaultCommand)
            self.database.Add_Unique_Command(defaultCommand,-1)

    def Command_Is_Invalid(self):

        f = open('invalidCommands.txt', 'r')

        invalidCommands = []

        for line in f:

            invalidCommands.append( line.rstrip() )

        f.close()

        return self.command in invalidCommands

    def No_Commands_Available_In_Database(self):
        return self.database.Get_Unique_Commands() == []

    def Set_Command_Issued_By_User(self):

        self.command = self.database.Get_Command_From_Queue()

        if (self.database.Command_Is_New(self.command)):

            self.database.Add_Unique_Command(self.command,0)

        self.database.Delete_Command_From_Queue()

    def Set_Random_Command(self):

        allAvailableCommands = self.database.Get_Unique_Commands()
        # print(allAvailableCommands)
        numCommands = len( allAvailableCommands )
        chosenCommandIndex = random.randint(0, numCommands-1)

        chosenCommand = allAvailableCommands[chosenCommandIndex]

        self.command = self.database.From_UniqueCommand_Record_Get_String( chosenCommand )

    def Set_Random_Command_Ranked(self):
        available_cmds = self.database.Get_Unique_Commands_Votes()
        num_votes = sum([cmd[1] for cmd in available_cmds])
        cmd_choice_index = random.randint(0, num_votes - 1)

        chosen_cmd = None
        for cmd, votes in available_cmds:
            if cmd_choice_index < votes:
                chosen_cmd = cmd
                break
            else:
                cmd_choice_index -= votes
        self.command = chosen_cmd

    def Set_Valid_Random_Command(self, ranked=False):

        if ranked:
            self.Set_Random_Command_Ranked()
        else:
            self.Set_Random_Command()

        while self.Command_Is_Invalid():
            if ranked:
                self.Set_Random_Command_Ranked()
            else:
                self.Set_Random_Command()
