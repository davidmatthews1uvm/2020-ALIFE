import sys
  
sys.path.insert(0, '..')

from database.database import DATABASE

db = DATABASE()

db.Add_User('joshb')
