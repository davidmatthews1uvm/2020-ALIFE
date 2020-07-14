import os
import sys

sys.path.insert(0, '..')

import copy

from school.student import STUDENT

parent = STUDENT(0)
parent.Evaluate(playBlind=True, playPaused=False)

for g in range(0, 10):
    child = copy.deepcopy(parent)
    child.Mutate()
    child.Evaluate(playBlind=True, playPaused=False)

    print(g, parent.Get_Fitness(), child.Get_Fitness())

    if (child.Is_More_Fit_Than(parent)):
        parent = child

parent.Evaluate(playBlind=False, playPaused=True)
