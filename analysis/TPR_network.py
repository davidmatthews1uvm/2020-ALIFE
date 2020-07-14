from sklearn.model_selection import KFold
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Input, Embedding, LSTM, Dense, Activation
import keras
from datetime import datetime
import copy
import pickle
import numpy as np
import time
import sys
import argparse
from scipy.stats.stats import ttest_ind
from keras import backend as K
import tensorflow as tf
import csv
import math

#job_seed = int(sys.argv[1])

reinforcements = pickle.load(open("all_move_reinforcements.p", 'rb'))
sensor_data = pickle.load(open("all_move_sensordata.p", 'rb'))

num_sensors , timesteps, num_robots = sensor_data.shape

#make the data smaller for debugging
#sensor_data = sensor_data[:,:,:50]
#reinforcements = reinforcements[:50]

#num_sensors , timesteps, num_robots = sensor_data.shape

print(sensor_data.shape)


def setup_network():
    sensor_input = Input(shape=(timesteps, num_sensors), name='sensor_input')
    lstm1 = LSTM(9, return_sequences=True)(sensor_input)
    dropout1 = Dropout(0.2)(lstm1)
    lstm2 = LSTM(9, return_sequences=False)(dropout1)
    dropout2 = Dropout(0.2)(lstm2)
    output = Dense(1, activation='tanh', name='output')(dropout2)
    model = Model(inputs=[sensor_input], outputs=[output])

    # compiling the model
    model.compile(
     optimizer = "adam",
     loss = "mean_squared_error",
     metrics = ['mae', 'acc']
    )
    
    return model



def train_model(model, train_x, train_y, test_x, test_y, e):
    results = model.fit(
     train_x, train_y,
     epochs= e,
     batch_size = 4,
     validation_data = (test_x, test_y)
    )



#running k folds and saving scores for man whitney
def run_critic(X, y, isControl):
    seed = 7
    np.random.seed(seed)

    num_of_folds = 30 
    num_of_epochs = 20

    kf = KFold(n_splits= num_of_folds)
    kf.get_n_splits(X)

    cvscores = []
    count = 0
    for train_index, test_index in kf.split(X):
        #This can be split by jobs, it will be num_of_folds jobs
        print("------------------------", count, "---------------------------")
        count += 1
        #split the sensor data differently each fold
        X_train, X_test = X[train_index], X[test_index]
        
        if isControl == True:
            #shuffle data each fold
            shuffled_y = y.copy()
            np.random.shuffle(shuffled_y)
            
            #split the reinforcements differently each fold
            y_train, y_test = shuffled_y[train_index], shuffled_y[test_index]
        
        else:
            #split the reinforcements differently each fold
            y_train, y_test = y[train_index], y[test_index]

        #train
        model = setup_network()
        train_model(model, X_train, y_train, X_test, y_test, num_of_epochs)
        scores = model.evaluate(X_test, y_test, verbose=0)
        for i in range(len(scores)):
            print("%s: %.2f%%" % (model.metrics_names[i], scores[i]*100))
        cvscores.append(scores)

    return cvscores



#with reinforcements between -1 and 1
X = np.transpose(sensor_data[:,:,:])
y = reinforcements[:]

#with reinforcements that are rounded to -1 or 1
y_bool = np.zeros(y.shape)
for i in range(len(y)):
    if y[i] > 0:
        y_bool[i] = 1
    if y[i] < 0:
        y_bool[i] = -1

#print(y)
#print(y_bool)
        

#if job_seed % 4 == 0:
    #produces 30 jobs
cvscores = run_critic(X,y,False)
with open('cvscores.p', 'wb') as f:
    pickle.dump(cvscores, f)
print("------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------")
#elif job_seed % 4 == 1:
#produces 30 jobs
cvscores_control = run_critic(X,y,True)
with open('cvscores_control.p', 'wb') as f:
    pickle.dump(cvscores_control, f)
print("------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------")

#elif job_seed % 4 == 2:
#produces 30 jobs
cvscores_bool = run_critic(X,y_bool,False)
with open('cvscores_bool.p', 'wb') as f:
    pickle.dump(cvscores_bool, f)
print("------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------")
#elif job_seed % 4 == 3:    
#produces 30 jobs
cvscores_bool_control = run_critic(X,y_bool,True)
with open('cvscores_bool_control.p', 'wb') as f:
    pickle.dump(cvscores_bool_control, f)
print("------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------")

