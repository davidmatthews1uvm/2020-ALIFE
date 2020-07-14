import sys

sys.path.insert(0, '..')

from TPR_3.population import POPULATION
from database.database import DATABASE

# ------------- Main function --------------------
 
if __name__ == "__main__":

    database = DATABASE()

    population = POPULATION(database, testing=False)

    while True:

        population.Perform_One_Simulation()
