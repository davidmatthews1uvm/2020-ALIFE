import sys
  
sys.path.insert(0, '..')

from database.database import DATABASE

db = DATABASE()

db.Set_PtsPerSec_For_User(0.5,0)
