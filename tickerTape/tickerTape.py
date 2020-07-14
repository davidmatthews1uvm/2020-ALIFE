import sys
  
sys.path.insert(0, "..")

import time

from tickerTape.screen import SCREEN

from tickerTape.message import MESSAGE

class TICKER_TAPE:

    def __init__(self,database,screen):

        self.database = database

        self.message = None

        self.screen = screen 

    def Update_Once(self):

        if self.message:

            self.message.Draw_To(self.screen)

            self.message.Move_To_The_Left()

            if self.message.Done():

                self.message = None 
        else:

            self.message = MESSAGE(self.database,self.screen) 
