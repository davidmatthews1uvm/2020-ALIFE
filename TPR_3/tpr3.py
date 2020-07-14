import sys
import os

sys.path.insert(0, '..')

from TPR_3.evolver import EVOLVER
from database.database import DATABASE

# -------------- Main function ------------------
if __name__ == "__main__":
    d = DATABASE()
    d.Reset()
    e = EVOLVER()

    while True:
        e.Perform_Ten_Evaluations()