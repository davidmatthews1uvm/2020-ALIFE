import os

import pygraphviz as pgv

import constants as c

class PHYLOTREE:

    def __init__(self):
        pass

    def Draw(self, aliveBots, primaryBotID, secondaryBotID):
        self.phyloTree = pgv.AGraph(bgcolor='black',label='?familyTree',fontcolor='white',fontsize=22)
        self.Add_Nodes(aliveBots, primaryBotID, secondaryBotID)
        self.Add_Edges(aliveBots)
        self.phyloTree.graph_attr.update(ratio="fill",size="3!")
        self.phyloTree.draw('../visualizations/pt.png', prog='dot')
        os.system("mv ../visualizations/pt.png ../visualizations/phyloTree.png")

    def Draw_Empty(self):
        self.phyloTree = pgv.AGraph(bgcolor='black')
        self.phyloTree.graph_attr.update(ratio="fill",size="3!")
        self.phyloTree.draw('../visualizations/pt.png', prog='dot')
        os.system("mv ../visualizations/pt.png ../visualizations/phyloTree.png")

    def Sufficient_Conditions_For_Drawing(self):
        return True

# --------------- Private methods -------------------

    def Add_Edges(self, aliveBots):
        for child in aliveBots:
            childID = aliveBots[child].ID
            parentID = aliveBots[child].parentID
            parentIsAlive = False

            for candidateParent in aliveBots:
                if ((child != candidateParent) and (aliveBots[candidateParent].ID == parentID)):
                    parentIsAlive = True

            if (parentIsAlive):
                self.phyloTree.add_edge(parentID, childID,color="white")
            else:
                self.phyloTree.add_edge(-1, childID,color="white")

    def Add_Node(self, aliveBots, r, primaryBotID, secondaryBotID):
        colorIndex = r
        nodeColor = c.colorNamesNoParens[colorIndex]

        if (nodeColor == 'silver'):
            nodeColor = 'gray'
        elif (nodeColor == 'green'):
            nodeColor = 'darkgreen'
        elif (nodeColor == 'jade'):
            nodeColor = 'palegreen'

        w = 0.1
        h = 0.1

        ID = aliveBots[r].ID

        if (ID == primaryBotID):
            w = 0.5
            h = 0.5
        elif (ID == secondaryBotID):
            w = 0.3
            h = 0.3

        if nodeColor == 'white':
            edgeColor = 'black'
        else:
            edgeColor = nodeColor

        self.phyloTree.add_node(aliveBots[r].ID, label="", fixedsize=False, width=w, height=h, style='filled',
                                color=edgeColor, fillcolor=nodeColor)

    def Add_Nodes(self, aliveBots, primaryBotID, secondaryBotID):
        self.phyloTree.add_node(-1, label="", fixedsize=False, width=0, height=0)

        for r in aliveBots:
            self.Add_Node(aliveBots, r, primaryBotID, secondaryBotID)
