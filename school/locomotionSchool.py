import os
import sys

import copy

sys.path.insert(0, '..')

from school.jbStudent import JBSTUDENT
import constants as c

def Compete_Parent_Against_Child(parents, children, s):
    if (children[s].Is_More_Fit_Than(parents[s])):
        parents[s] = children[s]
        parents[s].Save(s)

def End_Child(children,s):
    children[s].End_Evaluation()

def Evaluate_Best(parents, playBlind, playPaused):
    indexOfBest = -1
    valueOfBest = -1e99

    i = 0
    for robot in parents:
        if parents[robot].Get_Fitness() > valueOfBest:
            indexOfBest = i
            valueOfBest = parents[robot].Get_Fitness()
        i += 1

    parents[indexOfBest].Evaluate(playBlind=playBlind, playPaused=playPaused)

def Initialize(parents):
    for s in range(0, c.popSize):
        parents[s] = JBSTUDENT(s)

    for s in range(0, c.popSize):
        parents[s].Evaluate(playBlind=True, playPaused=False)
        parents[s].Save(s)

def Perform_One_Generation(parents):
    Save_And_Reset_Robots_If_Necessary()

    children = {}

    for s in parents:
        Spawn_Child_From_Parent(parents,children,s)

    for s in parents:
        Start_Child(children,s)

    for s in parents:
        End_Child(children,s)

    for s in parents:
        Compete_Parent_Against_Child(parents,children,s)

def Print(students):
    for s in students:
        print( str(students[s].Get_Fitness()) + ' ' , end='' )

    print()

#prints the fitness of the best agent in the population 
def Print_Best_Fitness(parents):
    indexOfBest = -1
    valueOfBest = -1e99
    
    i = 0
    for robot in parents:
        if parents[robot].Get_Fitness() > valueOfBest:
            indexOfBest = i
            valueOfBest = parents[robot].Get_Fitness()
        i += 1

    print(str(parents[indexOfBest].fitness), end="")

def Save_And_Reset_Robots_If_Necessary():
    for s in parents:
        parents[s].Save_And_Reset_If_Ancestor_Was_Harvested(s)


def Spawn_Child_From_Parent(parents,children,s):
    children[s] = copy.deepcopy(parents[s])
    children[s].Mutate()

def Start_Child(children,s):

    children[s].Start_Evaluation(playBlind=True, playPaused=False)

# ----------------- Main function -----------------------

parents = {}
Initialize(parents)
print("Initial Pop. ", end="")
Print(parents)

for i in range(0,100):
    Perform_One_Generation(parents)

    print("Gen", i, end=":  ")
    print("Best [", end="")

    print(Print_Best_Fitness(parents), end="] POP [")
    Print(parents)
    print("]", end="")

Evaluate_Best(parents, playBlind=False, playPaused=True)