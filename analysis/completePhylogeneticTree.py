import sys

sys.path.insert(0, '../database')
from database import DATABASE

sys.path.insert(0, '..')
import constants as c

import pygraphviz as pgv

db = DATABASE()

robots = db.Get_Robots()

phyloTree = pgv.AGraph()  # bgcolor='green')

# phyloTree.add_node(-1,label="", fixedsize=False, width=1,height=1)

for robot in robots:

    parentID = db.Get_Robot_Parent_ID(robot)

    childID = db.Get_Robot_ID(robot)

    numYeses = db.Get_Robot_Num_Yeses(childID)

    numNos = db.Get_Robot_Num_Nos(childID)

    numEvals = db.Get_Robot_Num_Evaluations(childID)

    isAlive = db.Get_Robot_Alive_Status(robot)

    nodeLabel = str(numEvals) + "," + str(numYeses) + "-" + str(numNos)

    colorIndex = db.Get_Robot_Color_Index(robot)

    nodeColor = c.colorNamesNoParens[colorIndex]

    edgeColor = 'black'

    if (nodeColor == 'silver'):

        nodeColor = 'gray'

    elif (nodeColor == 'green'):

        nodeColor = 'darkgreen'

    elif (nodeColor == 'jade'):

        nodeColor = 'palegreen'

    if (isAlive == False):
        nodeColor = 'white'
        edgeColor = 'white'

    phyloTree.add_node(childID, label=nodeLabel, fixedsize=False, style='filled', color=edgeColor, fillcolor=nodeColor)

    if (parentID > -1):
        phyloTree.add_edge(parentID, childID)

phyloTree.draw('completePhyloTree.png', prog='dot')
