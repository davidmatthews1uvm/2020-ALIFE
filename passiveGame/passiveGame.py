
from passiveGame.activeUsers import ACTIVE_USERS

from passiveGame.options import OPTIONS

from passiveGame.screen import SCREEN

class PASSIVE_GAME:

    def __init__(self,database):

        self.database = database 

        self.activeUsers = ACTIVE_USERS(self.database)

        self.options = OPTIONS(self.database)

        self.screen = SCREEN()

    def Done(self):

        return self.screen.Done()

    def Get_Screen(self):

        return self.screen

    def Update_Once(self):

        self.Update()

        # self.screen.Prepare()

        maxPts , ptsPerSec = self.activeUsers.Get_Max_Pts_And_Pts_Per_Sec()

        self.options.Draw_To(self.screen , self.activeUsers.Get_Highest_Score() , maxPts , ptsPerSec )

        self.activeUsers.Draw_To(self.screen)

        self.screen.Handle_Events()

        # self.screen.Reveal()

    def Update(self):

        self.options.Update()

        self.activeUsers.Update()
