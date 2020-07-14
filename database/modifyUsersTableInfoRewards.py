import sqlite3 as lite
import sys

sys.path.insert(0, "..")
from database.database import DATABASE

if __name__ == "__main__":
    db = DATABASE()
    
    strng = 'PRAGMA table_info(USERS)'
    db.Safe_Execute(strng)

    returnedInfo = db.cur.fetchall()

    try:
    	gotData = returnedInfo[8]
    except IndexError:
    	print("Adding StartInfoClaims column to USERS")
    	strng = 'ALTER TABLE USERS ADD StartInfoClaims Int DEFAULT(0)'
    	db.Safe_Execute(strng)

    try:
    	gotData = returnedInfo[9]
    except IndexError:
    	print("Adding EndInfoClaims column to USERS")
    	strng = 'ALTER TABLE USERS ADD EndInfoClaims Int DEFAULT(0)'
    	db.Safe_Execute(strng)