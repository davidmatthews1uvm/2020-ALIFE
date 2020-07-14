import numpy as np
import matplotlib.pyplot as plt 
from scipy import stats

import pickle

#reinforcements = pickle.load(open('data/Reinforcements_new.p','rb'))

#tensor = pickle.load(open('data/sensordata_new.p','rb'))
reinforcements = pickle.load(open('data/Reinforcements_move1.p','rb'))

tensor = pickle.load(open('data/sensordata_move1.p','rb'))

print(reinforcements.shape)

robots = len(tensor[0,0,:])
timesteps = len(tensor[0,:])
sensors = len(tensor[:])


def sensor_value_integration(tensor,reinforcements):
    
    robot_move_correlation = np.zeros(robots)
    x_y_z_sums = np.zeros([sensors,robots])
    timestep_averages = np.zeros([sensors,timesteps])
    for r in range(0,robots):
        for t in range(0,timesteps):
            current = tensor[:,t,r]
            past = tensor[:,t-1,r]
            timestep_averages[:,t] = abs(current - past)
            
        x_y_z_sums[0,r] = sum(timestep_averages[0,:])
        x_y_z_sums[1,r] = sum(timestep_averages[1,:])
        x_y_z_sums[2,r] = sum(timestep_averages[2,:])
    
    for r in range (0,robots):
        robot_move_correlation[r] = (x_y_z_sums[0,r] + x_y_z_sums[1,r] + x_y_z_sums[2,r])/3
        
    return robot_move_correlation

def plot(Xs,Ys):
    fig = plt.figure()
    print(stats.linregress(Xs,Ys))
    slope,intercept,r_value,p_value,std_err = stats.linregress(Xs,Ys)
    plt.scatter(Xs,Ys,alpha=.2,color='#FF0000')
    plt.plot(Xs,intercept+slope*Xs,color='#0000FF')
    plt.xlabel('Average Sensor Value Change Across Timesteps')
    plt.ylabel('Reinforcements')
    plt.show()
    fig.savefig('imgs/img4')

RMC = sensor_value_integration(tensor,reinforcements)
plot(RMC,reinforcements)    