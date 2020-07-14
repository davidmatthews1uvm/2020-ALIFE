import constants as c

import os

import sys

import time

class SPEECH:

    def __init__(self,command,positionsOfRobotsBeingSimulated):

        self.command = command

        self.positionsOfRobotsBeingSimulated = positionsOfRobotsBeingSimulated

    def start(self,speed):

        # time.sleep(1)

        self.Say_Short(speed)

        # self.Say_Long()

# --------------------- Private methods ------------------------

    def Simulating_All_Bots(self):

        return len(self.positionsOfRobotsBeingSimulated) == c.popSize

    def Say_Long(self):

        commandStr = self.command.Get_String()

        robotIndex = self.positionsOfRobotsBeingSimulated[0]

        robotColor = c.colors[robotIndex]

        robotColorName = c.colorNamesNoParens[robotIndex]

        speech = "The " + robotColorName + " robot is trying to jump. If you think it is, type " + robotColor + ". y."

        os.system('say ' + speech)

        speech = "If it is not, type " + robotColor + ". n."

        os.system('say ' + speech)

    def Say_Short(self,speed):

        commandStr = self.command.Get_String()

        newCommandStr = ''

        for word in commandStr.split():

            newCommandStr = newCommandStr + word + '. '
       
        commandStr = newCommandStr
 
        robotIndex = self.positionsOfRobotsBeingSimulated[0]

        robotColor = c.colors[robotIndex]

        speech =          commandStr

        #if not self.Simulating_All_Bots():

        stringToSay =               'say -v "Samantha" ' # -r ' + str(c.SPEECH_REINFORCEMENT_SPEED)
        stringToSay = stringToSay + '      ' + commandStr + '.'

        #    stringToSay = stringToSay + '      ' + robotColor.upper() + '...'
        #    stringToSay = stringToSay + ' Y... ' + '.'
        #    stringToSay = stringToSay + ' Or   ' + '.'
        #    stringToSay = stringToSay + '      ' + robotColor.upper() + '...' 
        #    stringToSay = stringToSay + ' N... ' + '.'
        os.system(stringToSay)

            #os.system('say -v "Samantha" ' # -r '+str(c.SPEECH_COMMAND_SPEED)      +' ' + commandStr)
            #os.system('say -v "Samantha" -r '+str(c.SPEECH_REINFORCEMENT_SPEED)+' ' + robotColor)
            #os.system('say -v "Samantha" -r '+str(c.SPEECH_REINFORCEMENT_SPEED)+' y')
            #os.system('say -v "Samantha" -r '+str(c.SPEECH_REINFORCEMENT_SPEED)+' or')
            #os.system('say -v "Samantha" -r '+str(c.SPEECH_REINFORCEMENT_SPEED)+' ' + robotColor)
            #os.system('say -v "Samantha" -r '+str(c.SPEECH_REINFORCEMENT_SPEED)+' n')
