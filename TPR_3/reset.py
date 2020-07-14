import os
import pickle
import sys

sys.path.insert(0, '..')

from database.database import DATABASE

from TPR_3.robot import ROBOT

import constants as c

def Collect_Robot_From_School(position):

    filename = "../school/students/student" + str(position) + ".p"

    robot = pickle.load(open(filename, 'rb'))

    Delete_Robot(position)

    robot.Set_ID(position)

    print('Robot ' + str(position) + ' collected from school.')

    return robot

def Create_Environments(database):

    for e in range(1, c.NUM_ENVIRONMENTS_AVAILABLE + 1):

        database.Add_Environment(e)

        print('Environment ' + str(e) + ' created.')

def Create_Initial_Population(database):

    for r in range(0, c.popSize):

        if Robot_Available_From_School(r):

            robot = Collect_Robot_From_School(r)
        else:
            robot = Create_Random_Robot(r)

        database.Add_Robot(robot)

def Create_Random_Robot(position):

    robot = ROBOT(database.Get_Next_Available_Robot_ID(),
        colorIndex=position,
        parentID=-1,
        clr=c.colorRGBs[position])

    print('Random robot ' + str(position) + ' created.')

    return robot


def Delete_Robot(position):
    filename = "../school/students/student" + str(position) + ".p"
    os.remove(filename)

def Empty_Data_Directory():

    os.system( 'rm ../data/*' )

    print('Emptied the data/ directory.')

def Reset_Database():
    d = DATABASE(silent_mode=True)
    d.Reset()
    print('The database is reset.')

    return d

def Robot_Available_From_School(position):

    filename = "../school/students/student" + str(position) + ".p"

    return os.path.isfile(filename)

def Unlock_First_Two_Environments(database):

    for e in range(1,2+1):

        database.Unlock_Environment(e)

        print('Environment ' + str(e) + ' unlocked.')

def Unlock_All_Robots(database):

    for ID in range(0,c.popSize):

        database.Unlock_Bot(ID)

        print( 'Robot ' + str(ID) + ' unlocked.' )

# ------------- Main function ------------------

Empty_Data_Directory()

database = Reset_Database()

Create_Initial_Population(database)

Unlock_All_Robots(database)

Create_Environments(database)

Unlock_First_Two_Environments(database)
