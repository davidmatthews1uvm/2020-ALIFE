import sys

sys.path.insert(0, '../database')
from database import DATABASE

sys.path.insert(0, '..')
import constants as c

import pygraphviz as pgv
import networkx as nx

db = DATABASE()

robots = db.Get_Robots()
#robots = robots[-500:]

phyloTree = pgv.AGraph()  # bgcolor='green')

#phyloTree.add_node(-1,label="", fixedsize=False, width=1,height=1)

for robot in robots:

    parentID = db.From_Robot_Record_Get_Parent_ID(robot)

    childID = db.From_Robot_Record_Get_ID(robot)

    numYeses = db.Get_Robot_Num_Yeses(childID)

    numNos = db.Get_Robot_Num_Nos(childID)

    numEvals = db.Get_Robot_Num_Evaluations(childID)

    isAlive = db.From_Robot_Record_Get_Alive_Status(robot)

    nodeLabel = str(childID)

    colorIndex = db.From_Robot_Record_Get_Color_Index(robot)

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
        #edgeColor = 'white'

    if numYeses > numNos:

        nodeColor = 'green'
    else:
        nodeColor = 'red'

    phyloTree.add_node(childID, label=nodeLabel, fixedsize=False, style='filled', color=edgeColor, fillcolor=nodeColor)

    if (parentID > -1):
        phyloTree.add_edge(parentID, childID)

nxGraph = nx.nx_agraph.from_agraph(phyloTree)

#nxGraph.remove_nodes_from(list(nx.isolates(nxGraph)))

#for component in list(nx.connected_components(nxGraph)):
#    if len(component)<25:
#        for node in component:
#            nxGraph.remove_node(node)

componentsSortedByDecreasingSize = sorted(nx.connected_components(nxGraph), key=len, reverse=True)

#giantComponent = max(nx.connected_components(nxGraph), key=len)
for node in list(nxGraph):
    if node not in componentsSortedByDecreasingSize[0] and node not in componentsSortedByDecreasingSize[1] and node not in componentsSortedByDecreasingSize[2] and node not in componentsSortedByDecreasingSize[3]:
        nxGraph.remove_node(node)

phyloTree = nx.nx_agraph.to_agraph(nxGraph)

phyloTree.draw('completePhyloTree.png', prog='dot')
