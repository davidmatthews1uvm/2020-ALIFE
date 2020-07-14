import sys

from database.database import DATABASE


def Send_Reinforcement(color, reinforcement):
    db = DATABASE()

    ID = db.Get_Most_Recent_Bot_With_Color(color)

    if (ID == -1):
        print('bot not found')
        return

    if (reinforcement == 'y'):
        print('bot ' + str(ID) + ' positively reinforced.')
    else:
        print('bot ' + str(ID) + ' negatively reinforced.')

    db.Add_Reinforcement(ID, reinforcement)


# ----------------------- Main method -----------------------

userInput = sys.argv[1]
color = userInput[0]
reinforcement = userInput[1]

Send_Reinforcement(color, reinforcement)
