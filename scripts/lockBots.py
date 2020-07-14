import random

import sys

sys.path.insert(0, "..")

import constants as c

from database.database import DATABASE

database = DATABASE()

def Population_Is_Full():

    pop = database.Get_Live_Robots()

    return len(pop) == c.popSize

def More_Than_Six_Bots_Unlocked():

    unlockedBots = database.Get_Unlocked_Robots()

    return len(unlockedBots) > 6 

def Lock_Bots():

    unlockedBots = database.Get_Unlocked_Robots()

    while len(unlockedBots) > 6:

        random.shuffle(unlockedBots)

        botToLock = unlockedBots.pop() 

        robotID = database.From_Robot_Record_Get_ID(botToLock)

        database.Lock_Bot(robotID)

def Locking_Required():

    return False # The un/locking of robots has currently been disabled.

    if database.Active_Users_Present():

        return False

    return Population_Is_Full() and More_Than_Six_Bots_Unlocked()

# -------------------- Main function -----------------------

if Locking_Required():

    Lock_Bots()
