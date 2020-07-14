import random

import sys

sys.path.insert(0, "..")

import constants as c

from database.database import DATABASE

database = DATABASE()

def All_But_Two_Envs_Locked():

    lockedEnvs = database.Get_Locked_Environments()

    return len(lockedEnvs) == c.NUM_ENVIRONMENTS_AVAILABLE - 2 

def Lock_Envs():

    for e in range(3,c.NUM_ENVIRONMENTS_AVAILABLE + 1):

        # Do not lock the first two environments...

        database.Lock_Environment(e)

def Locking_Required():

    if database.Active_Users_Present():

        return False

    if All_But_Two_Envs_Locked():

        return False

    return True

# -------------------- Main function -----------------------

if Locking_Required():

    Lock_Envs()
