import time

import sys
sys.path.append('..')

from reinforcements import REINFORCEMENTS

from robots import ROBOTS

from screen import SCREEN

class PARETO_FRONT:

    def __init__(self,database):

        self.timeOfLastPerSecondPerformance = time.time()

        self.screen = SCREEN()

        self.robots = ROBOTS(database,self.screen)

        self.reinforcements = REINFORCEMENTS()

    def Run_Forever(self,database):

        while not self.screen.Done():

            self.Try_To_Perform_Tasks_Once_Per_Second(database)

            self.Perform_Tasks_Every_Frame(database)

# ---------------- Private methods ------------------------

    def Perform_Tasks_Every_Frame(self,database):

        self.screen.Prepare()

        self.robots.Draw_Shadows()

        self.screen.Draw_Sun( self.robots.Get_Max_Losses() , self.robots.Get_Max_Wins() )

        self.screen.Add_Title()

        self.screen.Add_Axes()

        self.reinforcements.Update(database)

        self.reinforcements.Draw_To(self.screen.Get_Screen())

        self.robots.Draw_Circles()

        self.screen.Reveal()

    def Perform_Tasks_Every_Second(self,database):

        if self.reinforcements.Are_Empty():

           self.robots.Reset(database,self.screen)

           self.reinforcements.Load_New_Ones(database,self.robots)

    def Try_To_Perform_Tasks_Once_Per_Second(self,database):

        elapsedSecondsSinceLastExecution = time.time() - self.timeOfLastPerSecondPerformance

        if elapsedSecondsSinceLastExecution > 1:

            self.Perform_Tasks_Every_Second(database)

            self.timeOfLastPerSecondPerformance = time.time()

