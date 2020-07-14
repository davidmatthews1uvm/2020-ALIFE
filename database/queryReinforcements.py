import sys
import os

sys.path.insert(0, '..')

from database.database import DATABASE

if __name__ == "__main__":
    db = DATABASE()
    reinforcements = db.Get_Reinforcements()

    for reinforcement in reinforcements:
        print(reinforcement)