import random

import constants as c

import constantsPassiveGame as cpg

class MESSAGE():

    def __init__(self,database,screen):

        self.database = database

        messageRecord = self.database.Get_Oldest_Unprocessed_Message()

        if messageRecord:

            self.Add_Message_From_Database(messageRecord)

        else:
            self.Create_Random_Message()

        self.numberOfQueuedMessages = self.database.Get_Number_Of_Queued_Messages()

        self.horizontalPosition = cpg.width

        self.textsurface = screen.myfont.render(self.textOfMessage, True, (255,255,255))

        self.textrect = self.textsurface.get_rect()

        self.textrect.centery = cpg.depth + self.textrect.height/2

    def Done(self):

        return self.horizontalPosition < -self.textrect.width 

    def Draw_To(self,screen):

        self.textrect.centerx = self.horizontalPosition + self.textrect.width/2

        screen.screen.blit( self.textsurface , self.textrect )

    def Move_To_The_Left(self):

        self.horizontalPosition = self.horizontalPosition - c.tickerTapeSpeed * ( 1 + self.numberOfQueuedMessages )

# ------------ Private methods ----------------------

    def Add_Message_From_Database(self,messageRecord):

        ID  = self.database.From_Message_Record_Get_Id(messageRecord)

        self.textOfMessage = self.database.From_Message_Record_Get_Message(messageRecord)

        self.database.Delete_Message(ID)

    def Create_Random_Message(self):

        allKeys = list( c.tickerTapeRandomMessages.keys() )

        randomKey = random.choice(allKeys)

        if randomKey == 'unmuteMessage':

            self.textOfMessage = c.tickerTapeRandomMessages[randomKey]

        elif randomKey == 'missionMessage':

            self.textOfMessage = self.Modify_Mission_Message()
        else:
            self.textOfMessage = self.Modify_Best_Bot_Message()

    def Modify_Best_Bot_Message(self):

        colorIndex,BIndex = self.database.Get_Color_Index_And_Highest_B_Index_Among_Living_Robots()

        colorName = c.colorNamesNoParens[colorIndex]

        messageText = c.tickerTapeRandomMessages['bestBotMessage']

        textWithColorOfBestRobotIncluded = messageText.replace('YYY',colorName)

        textWithBIndexIncluded = textWithColorOfBestRobotIncluded.replace('XXX',str(BIndex))

        if BIndex == 1:
      
            textWithSingularOrPluralIncluded = textWithBIndexIncluded.replace('ZZZ','')
        else:
            textWithSingularOrPluralIncluded = textWithBIndexIncluded.replace('ZZZ','s')
 
        return textWithSingularOrPluralIncluded

    def Modify_Mission_Message(self):

        colorIndex,BIndex = self.database.Get_Color_Index_And_Highest_B_Index_Among_Living_Robots()

        targetBIndex = BIndex + 1

        messageText = c.tickerTapeRandomMessages['missionMessage']

        modifiedText = messageText.replace('XXX',str(targetBIndex))

        if targetBIndex == 1:

            textWithSingularOrPluralIncluded = modifiedText.replace('ZZZ','')
        else:
            textWithSingularOrPluralIncluded = modifiedText.replace('ZZZ','s')

        return textWithSingularOrPluralIncluded 
