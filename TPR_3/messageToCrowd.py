import constants as c

class MESSAGE_TO_CROWD:

    def __init__(self , simulationType , robots, robotPositions , commandString, speed, database, environmentIndex):

        self.simulationType = simulationType

        self.robots = robots

        self.robotPositions = robotPositions

        self.commandString = commandString

        self.commandsObeyedByBestBot = []

        self.speed = speed

        self.database = database

        self.environmentIndex = environmentIndex

    def Add_Command_Obeyed_By_Best_Bot(self,commandString):

        self.commandsObeyedByBestBot.append(commandString)

    def Print(self):

        self.Print_Preamble()

        # self.Print_Join_To_Start_Message()

        # self.Print_Unlocked_Message()

        if   self.simulationType == c.SIMULATE_DEATH:

            self.Print_Aggressor_Is_Killing_Defender()

        elif self.simulationType == c.SIMULATE_BIRTH_DE_NOVO:

            self.Print_Birth_De_Novo()

        elif self.simulationType == c.SIMULATE_BIRTH_FROM_AGGRESSOR:

            self.Print_Birth_From_Aggressor()

        elif self.simulationType == c.SIMULATE_ALL:

            self.Print_All_Message()

        elif self.simulationType == c.SIMULATE_BEST:

            self.Print_Best_Message()

        elif self.simulationType == c.SIMULATE_SURVIVAL:

            self.Print_Which_Is_Better_At()

            self.Print_Choices()

        elif self.simulationType == c.SIMULATE_DEATH_FROM_OLD_AGE:

            self.Print_Death_From_Old_Age_Message()

        #if self.database.Active_Users_Present(): 
        #    self.Print_Command()
        #    self.Print_Reinforcement()
        #    #self.Print_Environment()
        #    #self.Print_Current_Speed()
        #    self.Print_Event_Description()
        #    #self.Print_Help()
        #else:
        #    self.Print_Blank()
        #    self.Print_Blank()
        #    #self.Print_Blank()
        #    #self.Print_Blank()
        #    self.Print_Blank()
        #    #self.Print_Help()

    def Print_Command(self):
        print("!" + self.commandString)

    def Print_Current_Speed(self):
        print("speed: " + str(self.speed) + "x")

    def Print_Environment(self):

        print("environment: " + str(self.environmentIndex) )

    def Print_Event_Description(self):

        colorName = c.colorNamesNoParens[self.robotPositions[0]]

        if self.simulationType == c.SIMULATE_BIRTH_DE_NOVO:

            print(colorName + " is spawning as a new random bot!")

        elif self.simulationType == c.SIMULATE_BIRTH_FROM_AGGRESSOR:

            parentName = c.colorNamesNoParens[self.robotPositions[1]]

            print(parentName + " is spawning a " + colorName + " child!")

        elif self.simulationType == c.SIMULATE_DEATH:

            defenderName = c.colorNamesNoParens[self.robotPositions[1]]

            print(colorName + " is killing " + defenderName + "!")

        elif self.simulationType == c.SIMULATE_ALL:

            print("These are all the current bots.")

        elif self.simulationType == c.SIMULATE_BIRTH_FROM_DYING_PARENT:

            print(colorName + " is dying of age and being replaced by an offspring!")

        else:
            print("")

    def Print_Reinforcement(self):
        colorLetter = c.colors[self.robotPositions[0]]

        if ( (self.simulationType != c.SIMULATE_ALL) and (self.simulationType != c.SIMULATE_ALL_ORIGINAL_BOTS) ):

            print("" + colorLetter + "y / " + colorLetter + "n")
        else:
            print('')

    def Print_Blank(self):
        print()

    def Print_Help(self):
        print("New? Type anything to unlock more bots!")


        # self.Print_Terse()

        #botColorName = c.colorNames[self.robotPositions[0]]

        #if ( self.simulationType == c.SIMULATE_SURVIVAL ):

        #    print('This is the     ' + botColorName + ' bot.')

        #elif ( self.simulationType == c.SIMULATE_BIRTH_DE_NOVO ):

        #    print('This is the new ' + botColorName + ' bot, just spawned from scratch.')

        #elif ( self.simulationType == c.SIMULATE_BIRTH_FROM_AGGRESSOR ):

        #    print('This is the new ' + botColorName + ' bot, just spawned by the bot above.')

        #elif ( self.simulationType == c.SIMULATE_DEATH ):

        #    print('This is the     ' + botColorName + ' bot, which just killed the bot above.')

        #elif ( self.simulationType == c.SIMULATE_ALL ):

        #    print('These are all of the current bots attempting to !' + self.commandString + '.')

        #    print('')

        #    print('How are they doing?')

        #    for i in range(0,6):

        #         print('')
        #else:

        #    print('These are all of the original bots attempting to !' + self.commandString + '.')

        #    print('')

        #    print('(Do not reinforce these.)')

        #    for i in range(0,6):

        #         print('')

        #if ( (self.simulationType != c.SIMULATE_ALL) and (self.simulationType != c.SIMULATE_ALL_ORIGINAL_BOTS) ):

        #    self.Print_Info()

# -------------- Private methods -------------------------

    def Print_All_Message(self):

        whiteEscapeCode = "\u001b[38;5;231m"

        print(whiteEscapeCode + 'All bots responding to *' + str(self.commandString) + '.')

        for i in range(0,9):

            print('')

    def Print_Aggressor_Is_Killing_Defender(self):

        aggressorColorLetter = c.colors[self.robotPositions[1]]
        aggressorEscapeCode  = c.colorLetterToEscapeCode[aggressorColorLetter]

        whiteEscapeCode = "\u001b[38;5;231m"

        defenderColorLetter  = c.colors[self.robotPositions[0]]
        defenderEscapeCode   = c.colorLetterToEscapeCode[defenderColorLetter]

        print(whiteEscapeCode + \

            aggressorColorLetter + \

            ' is killing ' + \

            defenderColorLetter + \

            '.' )

        for i in range(0,9):

            print('')

    def Print_Best_Message(self):

        whiteEscapeCode = "\u001b[38;5;231m"

        print(whiteEscapeCode + 'The best bot responding to two commands')

        colorIndex, BIndex = self.database.Get_Color_Index_And_Highest_B_Index_Among_Living_Robots() 

        print('')

        print('randomly chosen from the ' + str(BIndex) + ' it obeys so far.')

        for i in range(0,3):
            print('')

        print('*' + self.commandsObeyedByBestBot[1])

        for i in range(0,2):
            print('')

        print('*' + self.commandsObeyedByBestBot[0] + ',')

    def Print_Birth_De_Novo(self):

        whiteEscapeCode = "\u001b[38;5;231m"

        defenderColorLetter  = c.colors[self.robotPositions[0]]
        defenderEscapeCode   = c.colorLetterToEscapeCode[defenderColorLetter]

        print(whiteEscapeCode + 'A new ' + \

            defenderEscapeCode + \

            defenderColorLetter  + \

            whiteEscapeCode + \

            ' is spawning from scratch.')

        print('')

    def Print_Birth_From_Aggressor(self):

        aggressorColorLetter = c.colors[self.robotPositions[1]]
        aggressorEscapeCode  = c.colorLetterToEscapeCode[aggressorColorLetter]

        whiteEscapeCode = "\u001b[38;5;231m"

        defenderColorLetter  = c.colors[self.robotPositions[0]]
        defenderEscapeCode   = c.colorLetterToEscapeCode[defenderColorLetter]

        print(whiteEscapeCode + \

            aggressorColorLetter + \

            ' is spawning a new ' + \

            defenderColorLetter + \

            '.' )

        for i in range(0,9):

            print('')

    def Print_Death_From_Old_Age_Message(self):

        #Color of dying parent == color of child
        robotColorLetter = c.colors[self.robotPositions[0]]
        robotEscapeCode  = c.colorLetterToEscapeCode[robotColorLetter]

        whiteEscapeCode = "\u001b[38;5;231m"

        print(robotEscapeCode + \

            robotColorLetter + \

            whiteEscapeCode + \

            ' is dying from old age (lived for ' + str(c.deathAge) + ' days)')

    def Print_Choices(self):

        aggressorColorLetter = c.colors[self.robotPositions[1]]

        defenderColorLetter  = c.colors[self.robotPositions[0]]

        escapeCode = c.colorLetterToEscapeCode[aggressorColorLetter]

        for i in range(0,3):
            print('')

        print(' ' + escapeCode + aggressorColorLetter)

        escapeCode = c.colorLetterToEscapeCode[defenderColorLetter]

        for i in range(0,2):
           print('')

        print(' ' + escapeCode + defenderColorLetter)

    def Print_Info(self):

        colorLetter = c.colors[self.robotPositions[0]]

        print('')

        print('It was just told to !' + self.commandString + '.')
        print('')

        print('Type             ' + colorLetter + 'y   if it is.')
        print('')

        print('Type             ' + colorLetter + 'n   otherwise.')
        print('')

        print('Type             ?    to learn more.')

    def Print_Preamble(self):

        for i in range(0,100):

            print('')

    def Print_Terse(self):

        colorLetter = c.colors[self.robotPositions[0]]

        print('!' + self.commandString)

        if ( (self.simulationType != c.SIMULATE_ALL) and (self.simulationType != c.SIMULATE_ALL_ORIGINAL_BOTS) ):

            print( colorLetter + 'y / ' + colorLetter + 'n')
        else:
            print('')

        print('Type ? for help.')

    def Print_Join_To_Start_Message(self):

        print('!Play to join.')

    def Print_Unlocked_Message(self):

        unlockedBots = self.database.Get_Unlocked_Robots()
        numUnlockedBots = len(unlockedBots)
        numLockedBots = c.popSize - numUnlockedBots
 
        print( str(numLockedBots) + ' bots still hidden!' )
        #print( str(numUnlockedBots) + ' of ' + str(c.popSize) + ' bots unlocked.')

        unlockedEnvs = self.database.Get_Unlocked_Environments()
        numUnlockedEnvs = len(unlockedEnvs)
        numLockedEnvs = c.popSize - numUnlockedEnvs

        print( str(numLockedEnvs) + ' environments still hidden!' )
        #print( str(numUnlockedEnvs) + ' of 10 environments unlocked.')

    def Print_Which_Is_Better_At(self):

        escapeCode = "\u001b[38;5;231m"

        # escapeCode = "\033[1;" + c.colorLetterToEscapeCode['w'] + ";40m"

        print( escapeCode + 'Which is better at')

        print('')

        print( escapeCode + '*' + self.commandString + '?' )

