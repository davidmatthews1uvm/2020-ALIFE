import sys
import os

sys.path.insert(0, '..')

from database.database import DATABASE

if __name__ == "__main__":
    db = DATABASE()
    db.Delete_Bad_Commands()
