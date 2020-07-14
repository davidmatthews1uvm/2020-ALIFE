import sys
  
sys.path.insert(0, '..')

from database.database import DATABASE

db = DATABASE()

db.Add_Chat_Message('?', 'joshb')

db.Add_User('joshb')
