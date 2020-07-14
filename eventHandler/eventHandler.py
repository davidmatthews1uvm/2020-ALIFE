import sys
sys.path.append('..')

import time

import constants as c

from database.database import DATABASE 

from passiveGame.passiveGame import PASSIVE_GAME 

from tickerTape.tickerTape import TICKER_TAPE

class EVENT_HANDLER():

    def __init__(self):

        self.database    = DATABASE()

        self.passiveGame = PASSIVE_GAME(self.database)

        self.tickerTape  = TICKER_TAPE(self.database , self.passiveGame.Get_Screen() )

    def Not_Done(self):

        return True # not self.passiveGame.Done()

    def Run_Forever(self):

        while self.Not_Done():

            self.Attempt_Frequent_Tasks()

    def Attempt_Frequent_Tasks(self):

        self.passiveGame.Get_Screen().Prepare()

        self.passiveGame.Update_Once()

        self.tickerTape.Update_Once()

        self.passiveGame.Get_Screen().Reveal()

# ---------- Main function -----------

eventHandler = EVENT_HANDLER()

eventHandler.Run_Forever()

