import random
import time

import matplotlib.pyplot as plt
import numpy as np


def Pick_Pair():
    first = random.randint(0, 50 - 1)
    second = random.randint(0, 50 - 1)

    while (second == first):
        second = random.randint(0, 50 - 1)

    return first, second


def Initialize():
    dots = np.random.randint(0, 100, [2, 50])
    x = dots[0]
    y = dots[1]
    plt.ion()
    fig = plt.figure()
    fig.patch.set_facecolor((0, 1, 0))
    ax = fig.add_subplot(111, axisbg=(0, 1, 0))
    scatter, = ax.plot(x, y, 'ko')  # Returns a tuple of line objects, thus the comma
    state = 0

    return dots, x, y, fig, ax, scatter, state


def Find_Victor_and_Victim(first, second, x, y):
    if ((x[first] < x[second]) and (y[first] < y[second])):
        return first, second
    else:
        return second, first


def Replace_Victim_With_Mutant_From_Victor(victor, victim, x, y):
    x[victim] = random.randint(x[victor] - 3, x[victor] + 3)

    if (x[victim] < 0):
        x[victim] = 0
    elif (x[victim] > 100):
        x[victim] = 100

    y[victim] = random.randint(y[victor] - 3, y[victor] + 3)

    if (y[victim] < 0):
        y[victim] = 0
    elif (y[victim] > 100):
        y[victim] = 100


# ------------ Main function -----------------

[dots, x, y, fig, ax, scatter, state] = Initialize()

while True:
    [first, second] = Pick_Pair()
    [victor, victim] = Find_Victor_and_Victim(first, second, x, y)
    Replace_Victim_With_Mutant_From_Victor(victor, victim, x, y)
    scatter.set_xdata(x)
    scatter.set_ydata(y)
    fig.canvas.draw()
    time.sleep(1)