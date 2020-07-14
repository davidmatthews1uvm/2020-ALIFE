import sys
import numpy as np
import os
import math
import pickle
sys.path.insert(0, "..")
#sys.path.insert(0,'../TPR_3')

from database.database import DATABASE
import pyrosim.pyrosim as pyrosim

from environments.environment0 import ENVIRONMENT0

import constants as c

NEW_DATABASE = False
if (NEW_DATABASE):
    from TPR_3.robot import ROBOT
else:
    sys.path.insert(0, '../TPR_3')
    from robot import ROBOT


dirname = '../data'
myfiles = os.listdir(dirname) # returns a list
robots = len(myfiles) -1

#only using xyz of pos sensor (size 3)
sensors = 3
timesteps = c.evaluationTime
db = DATABASE()

'''
pick whether you want a single unique command or all of the commands given (you may need to get rid of multiword/unwanted to commands)
'''
unique_commands = ([c[0] for c in db.Get_Unique_Commands()])
print(unique_commands)
#command = 'move'


def create_reinforcement_array(robots,command):
    '''    
    find the number of yes and no reinforcements from a robot
    normalize the difference using a method on page 5 from Mahoor,Felag,Bongard

    '''
    Yes_Per_Robot = np.zeros(robots)
    No_Per_Robot = np.zeros(robots)
    Reinforcements = np.zeros(robots)

    for i in range(robots):
        Yes_Per_Robot[i] = db.Get_Yes_Votes_For_Robot_Under_Command(i,command)
        No_Per_Robot[i] = db.Get_No_Votes_For_Robot_Under_Command(i,command)
        print(i)
    for i in range(0,robots):
        Reinforcements[i] = ((abs(Yes_Per_Robot[i])-abs(No_Per_Robot[i]))/(abs(Yes_Per_Robot[i])+abs(No_Per_Robot[i])))
    
    return Reinforcements

class robot_work(object):
    def __init__(self, sensors, timesteps, robotId, command):
        self.sensors = sensors
        self.timesteps = timesteps
        self.robotId = robotId
        self.command = command
        self.data = None

    def do_work(self):
        return create_tensor_helper(self.sensors, self.timesteps, self.robotId, self.command)

def create_tensor_helper(sensors, timesteps, robot, command):
    filename = '../data/robot{}.p'.format(robot)

    s = pyrosim.Simulator(debug=False, play_paused=False, eval_time=c.evaluationTime, play_blind=True)

    e = ENVIRONMENT0(s)

    e.Send_To_Simulator([0, 0, 0], [0, 0, 0], c.noFade)

    r = pickle.load(open(filename, 'rb'))

    commandEncoding = db.Get_Command_Encoding(command)
    if not NEW_DATABASE:
        commandEncoding = np.array([[commandEncoding]])

    # print(commandEncoding)
    word_vector = np.zeros(len(commandEncoding[0, :]))

    for i in range(0, len(commandEncoding[0, :])):
        # print(i,':',commandEncoding[:,i])
        word_vector[i] = commandEncoding[:, i]
    r.Send_To_Simulator(s, [0, 0, 0], [0, 0, 0], c.noFade, commandEncoding[0][0], old_format=True)

    s.assign_collision('robot', 'env')

    s.assign_collision('env', 'env')
    s.start()
    s.wait_to_finish()

    print(robot, end=", ", flush=True)
    return (robot, s.get_sensor_data(-1), s.get_sensor_data(-2), s.get_sensor_data(-3))


def create_tensor(sensors,timesteps,robots,command):
    '''
    the position sensor is the last sensor in the tree so this takes the xyz of position sensor and creates a tensor
    '''
    import multiprocessing

    pool = multiprocessing.Pool()

    work_to_do = list([robot_work(sensors, timesteps, r, command) for r in range(0, robots)])
    res = [pool.apply_async(w.do_work) for w in work_to_do]

    robots_dat = [r.get() for r in res]

    tensor = np.zeros([sensors,timesteps,robots])

    for r_id, x, y, z in robots_dat:
        tensor[0, :, r_id] = x
        tensor[1, :, r_id] = y
        tensor[2, :, r_id] = z

    commandEncoding = db.Get_Command_Encoding(command)
    if not NEW_DATABASE:
        commandEncoding = np.array([[commandEncoding]])

    # print(commandEncoding)
    word_vector = np.zeros(len(commandEncoding[0, :]))

    for i in range(0, len(commandEncoding[0, :])):
        # print(i,':',commandEncoding[:,i])
        word_vector[i] = commandEncoding[:, i]
    pool.close()
    return tensor,word_vector

def clean_tensor_and_reinforcements(tensor,reinforcements):
    '''
    deletes robots with a nan or inf value in their sensor data or normalized reinforcement value
    '''
    bad_robots = []

#    for r in range(0,robots):
#        for t in range (0,timesteps):
#            for s in range(0,sensors):
#                if math.isinf(tensor[s,t,r]):
#                    print(s,",",t,",",r)
#                    bad_robots.append(r)
#                if math.isnan(tensor[s,t,r]):
#                    print(s,",",t,",",r)
#                    bad_robots.append(r)

    for r in range(0,robots):
        if math.isinf(reinforcements[r]):
            bad_robots.append(r)
            print('rein',r)
        if math.isnan(reinforcements[r]):
            bad_robots.append(r)
            print('rein',r)
    tensor = np.delete(tensor,bad_robots,axis = 2)
    reinforcements = np.delete(reinforcements,bad_robots)
    return tensor,reinforcements

for com in unique_commands:
    print(com)
    reinforcements = create_reinforcement_array(robots,com)

    tensor,word_vector= create_tensor(sensors,timesteps,robots,com)

    tensor,reinforcements = clean_tensor_and_reinforcements(tensor,reinforcements)
    pickle.dump(reinforcements,open('Reinforcements_{}.p'.format(com),'wb'))
    pickle.dump(tensor,open('sensordata_{}.p'.format(com),'wb'))
    pickle.dump(word_vector,open('word_vector_{}.p'.format(com),'wb'))

#
#reinforcements = create_reinforcement_array(robots,c.defaultCommand)
#tensor,word_vector = create_tensor(sensors,timesteps,robots,c.defaultCommand)
#print('here')
#tensor,reinforcements = clean_tensor_and_reinforcements(tensor,reinforcements)
#
#    
#pickle.dump(reinforcements,open('Reinforcements_newer.p','wb'))
#pickle.dump(tensor,open('sensordata_newer.p','wb'))
#pickle.dump(word_vector,open('word_vector_newer.p','wb'))
#
#