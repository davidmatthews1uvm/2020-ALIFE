import sys
import os

sys.path.insert(0, '..')

from database.database import DATABASE

if __name__ == "__main__":
    db = DATABASE()
    users = db.Get_Users()

    for user in users:
        print(user)
