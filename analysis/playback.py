import sys

sys.path.insert(0, '../database')
from database import DATABASE

sys.path.insert(0, '../pyrosim')
import pyrosim

sys.path.insert(0, '../TPR_3')

sys.path.insert(0, '../environments')
from environment0 import ENVIRONMENT0

import constants as c

import pickle

database = DATABASE()

filename = '../data/robot0.p'

s = pyrosim.Simulator(debug=False, play_paused=False, eval_time=c.evaluationTime)

e = ENVIRONMENT0(s, [0, 0, 0], [0, 0, 0], c.noFade)

e.Send_To_Simulator()

r = pickle.load(open(filename, 'rb'))

command = c.defaultCommand
 
commandEncoding = database.Get_Command_Encoding(command)

r.Send_To_Simulator(s, [0, 0, 0], [0, 0, 0], c.noFade, commandEncoding)

s.assign_collision('robot', 'env')

s.assign_collision('env', 'env')

s.start()
