import pickle
import numpy as np

#oldest data
reinforcements1 = pickle.load(open("data/Reinforcements_move1.p", 'rb'))
sensor_data1 = pickle.load(open("data/sensordata_move1.p", 'rb'))

#newer data
reinforcements2 = pickle.load(open("data/Reinforcements_move2.p", 'rb'))
sensor_data2 = pickle.load(open("data/sensordata_move2.p", 'rb'))

#newest data
reinforcements3 = pickle.load(open("data/Reinforcements_move3.p", 'rb'))
sensor_data3 = pickle.load(open("data/sensordata_move3.p", 'rb'))

print(reinforcements1.shape)
print(reinforcements2.shape)
print(reinforcements3.shape)

reinforcements_move = np.concatenate((reinforcements1, reinforcements2),axis=0)
sensor_data_move = np.concatenate((sensor_data1, sensor_data2), axis = 2)

reinforcements_move = np.concatenate((reinforcements_move, reinforcements3),axis=0)
sensor_data_move = np.concatenate((sensor_data_move, sensor_data3), axis = 2)


pickle.dump(reinforcements_move, open('all_move_reinforcements.p', 'wb'))
pickle.dump(sensor_data_move, open('all_move_sensordata.p', 'wb'))