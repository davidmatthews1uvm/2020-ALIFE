import copy
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from database.database import DATABASE


class CUMULATIVE_YES_VOTES:

    def __init__(self):
        mpl.rcParams.update(mpl.rcParamsDefault)
        self.numBins = 5
        self.maxCommands = 6
        self.database = DATABASE()
        self.Get_Time_Of_First_And_Last_Reinforcement()

    def Collect_Data(self):
        self.Get_Yes_Votes()
        self.Sum_Yes_Votes()

    def Save(self):
        self.Prep_Figure()
        self.Draw_Figure()
        self.Annotate_Figure()
        plt.savefig('test.png', facecolor=self.fig.get_facecolor(), transparent=True)
        plt.close()

    def Sufficient_Conditions_For_Drawing(self):
        return self.totalSecondsOfExperiment > self.numBins

    # ------------------ Private methods -------------------------

    def Annotate_Figure(self):
        handles, labels = self.ax.get_legend_handles_labels()

        xTicks = [0, self.numBins]
        xTickLabels = ['Start', 'Now']

        plt.yticks([0, self.allYesses])

        plt.xticks(xTicks, xTickLabels)
        plt.ylabel('All yes votes')
        self.ax.legend(handles[::-1], labels[::-1], loc='upper left',fontsize=18)

    def Draw_Figure(self):

        self.allYesses = 0

        x = np.arange(self.numBins)
        previousHeights = np.zeros(self.numBins, dtype='f')

        numCommandsDrawn = 0

        for command in sorted(self.summedYesVotes, key=self.summedYesVotes.get, reverse=False):

            randomColor = np.random.random(3)
            yesses = int(self.summedYesVotes[command])
            self.allYesses = self.allYesses + yesses
            labelString = '!' + command + ': ' + str(yesses)

            self.ax.bar(x, self.yesVotes[command], width=1, bottom=previousHeights, color=randomColor,
                        edgecolor=randomColor, label=labelString)

            previousHeights = previousHeights + copy.deepcopy(self.yesVotes[command])

            numCommandsDrawn = numCommandsDrawn + 1

            if ( numCommandsDrawn == 7 ):

                break

    def Get_Time_Of_First_And_Last_Reinforcement(self):
        reinforcements = self.database.Get_Reinforcements()

        if (reinforcements == []):
            self.totalSecondsOfExperiment = 0
            return

        firstReinforcement = reinforcements[0]
        lastReinforcement = reinforcements[len(reinforcements) - 1]
        timeOfFirstReinforcementAsString = self.database.From_Reinforcement_Record_Get_Time(firstReinforcement)
        timeOfLastReinforcementAsString = self.database.From_Reinforcement_Record_Get_Time(lastReinforcement)
        self.timeOfFirstReinforcement = timeOfFirstReinforcementAsString # datetime.strptime(timeOfFirstReinforcementAsString, '%Y-%m-%d %H:%M:%S')
        self.timeOfLastReinforcement = timeOfLastReinforcementAsString # datetime.strptime(timeOfLastReinforcementAsString, '%Y-%m-%d %H:%M:%S')
        self.totalSecondsOfExperiment = int(
            (self.timeOfLastReinforcement - self.timeOfFirstReinforcement).total_seconds())

    def Get_Yes_Votes(self):
        self.yesVotes = {}
        self.commandsExtractedSoFar = 0
        reinforcements = self.database.Get_Reinforcements()

        for reinforcement in reinforcements:
            self.Handle_Reinforcement(reinforcement)

    def Handle_Positive_Reinforcement(self, reinforcement):
        evaluationID = self.database.From_Reinforcement_Record_Get_Evaluation_ID(reinforcement)
        evaluation = self.database.Get_Evaluation_Where_ID_Equals(evaluationID)
        command = self.database.From_Evaluation_Record_Get_Command(evaluation)
        timeOfReinforcementAsString = self.database.From_Reinforcement_Record_Get_Time(reinforcement)
        timeOfReinforcement = datetime.strptime(timeOfReinforcementAsString, '%Y-%m-%d %H:%M:%S')
        timeElapsedSinceStartOfExperiment = timeOfReinforcement - self.timeOfFirstReinforcement
        secondsElapsedSinceStartOfExperiment = int(timeElapsedSinceStartOfExperiment.total_seconds())
        bin = int(secondsElapsedSinceStartOfExperiment * (self.numBins - 1) / self.totalSecondsOfExperiment)

        if (self.New_Command(command)):
            self.Handle_New_Command(command, bin)
        else:
            self.Handle_Existing_Command(command, bin)

    def Handle_Existing_Command(self, command, bin):
        self.yesVotes[command][bin] = self.yesVotes[command][bin] + 1

    def Handle_New_Command(self, command, bin):
        if (self.Room_For_More_Commands()):
            self.yesVotes[command] = np.zeros(self.numBins, dtype='d')
            self.commandsExtractedSoFar = self.commandsExtractedSoFar + 1
            self.Handle_Existing_Command(command, bin)

    def Handle_Reinforcement(self, reinforcement):
        if self.Reinforcement_Is_Positive(reinforcement):
            self.Handle_Positive_Reinforcement(reinforcement)

    def New_Command(self, command):
        return command not in self.yesVotes

    def Prep_Figure(self):
        plt.rcParams.update({'font.size': 22})
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig.patch.set_alpha(0.0)

    def Reinforcement_Is_Positive(self, reinforcement):
        signal = self.database.From_Reinforcement_Record_Get_Signal(reinforcement)
        return signal == 'y'

    def Room_For_More_Commands(self):
        return self.commandsExtractedSoFar < self.maxCommands

    def Show(self):
        self.Prep_Figure()
        self.Draw_Figure()
        self.Annotate_Figure()
        plt.show()

    def Sufficient_Conditions_For_Drawing(self):
        return self.totalSecondsOfExperiment > self.numBins

    def Sum_Yes_Votes(self):
        self.summedYesVotes = {}

        for command in self.yesVotes:
            self.summedYesVotes[command] = sum(self.yesVotes[command])

        for command in self.yesVotes:
            for i in range(1, len(self.yesVotes[command])):
                self.yesVotes[command][i] = self.yesVotes[command][i] + self.yesVotes[command][i - 1]
