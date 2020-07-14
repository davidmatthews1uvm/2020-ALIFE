import random

import sys

import constants as c


#from environments.environment0 import ENVIRONMENT0

from environments.environment1 import ENVIRONMENT1
from environments.environment2 import ENVIRONMENT2
from environments.environment3 import ENVIRONMENT3
from environments.environment4 import ENVIRONMENT4
from environments.environment5 import ENVIRONMENT5
from environments.environment6 import ENVIRONMENT6
from environments.environment7 import ENVIRONMENT7
from environments.environment8 import ENVIRONMENT8
from environments.environment9 import ENVIRONMENT9

#from environments.env_ball import ENV_BALL
#from environments.env_monkeybars import ENV_MONKEYBARS
#from environments.env_ramp import ENV_RAMP
#from environments.env_seesaw import ENV_SEESAW
#from environments.env_slingshot import ENV_SLINGSHOT
#from environments.env_stairs import ENV_STAIRS
#from environments.env_cube_greenandred_front import ENV_CUBE_GREENANDRED_FRONT
#from environments.env_cube_green_front import ENV_CUBE_GREEN_FRONT
#from environments.env_cube_green_front_immobile import ENV_CUBE_GREEN_FRONT_IMMOBILE
#from environments.env_cube_green_left import ENV_CUBE_GREEN_LEFT

class ENVIRONMENT:

    def __init__(self , database, s ):

        self.database = database

        self.Find_Unlocked_Environment()

        if ( self.environmentIndex == 1 ):

            self.environment = ENVIRONMENT1( s )

        elif ( self.environmentIndex == 2 ):

            self.environment = ENVIRONMENT2( s )

        elif ( self.environmentIndex == 3 ):

            self.environment = ENVIRONMENT3( s )

        elif ( self.environmentIndex == 4 ):

            self.environment = ENVIRONMENT4( s )

        elif ( self.environmentIndex == 5 ):

            self.environment = ENVIRONMENT5( s )

        elif ( self.environmentIndex == 6 ):

            self.environment = ENVIRONMENT6( s )

        elif ( self.environmentIndex == 7 ):

            self.environment = ENVIRONMENT7( s )

        elif ( self.environmentIndex == 8 ):

            self.environment = ENVIRONMENT8( s )

        else:
            self.environment = ENVIRONMENT9( s )

    def Get_Index(self):

        return self.environmentIndex

    def Get_Robot_Offset(self):

        return self.environment.Get_Robot_Offset()

    def Print(self):

        print(self.environmentIndex)

    def Send_To_Simulator(self,physicsOffset , drawOffset , fadeStrategy):

        self.environment.Send_To_Simulator(physicsOffset , drawOffset , fadeStrategy)

# --------------------- Private methods ---------------------------

    def Find_Unlocked_Environment(self):

        self.environmentIndex = random.randint( 1 , c.NUM_ENVIRONMENTS_AVAILABLE ) 

        while self.database.Environment_Is_Locked(self.environmentIndex):

            self.environmentIndex = random.randint( 1 , c.NUM_ENVIRONMENTS_AVAILABLE )
