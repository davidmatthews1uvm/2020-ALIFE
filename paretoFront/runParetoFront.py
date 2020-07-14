import sys
  
sys.path.insert(0, '..')

from database.database import DATABASE

from paretoFront import PARETO_FRONT

database = DATABASE()

pf = PARETO_FRONT(database)

pf.Run_Forever(database)
