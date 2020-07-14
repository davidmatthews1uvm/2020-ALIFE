from __future__ import print_function

import os
import sys
from builtins import input

sys.path.insert(0, '..')

from database.database import DATABASE

if __name__ == "__main__":
    db = DATABASE()

    if len(sys.argv) == 2:
        command = sys.argv[1]
    else:
        command = input("enter a command to get details about: ")
    # command = "jump"
    numb_y = 0
    numb_n = 0

    execution_string = "SELECT * FROM Evaluations"
    db.cur.execute(execution_string)
    ttl_num_evals = len(db.cur.fetchall())

    execution_string = "SELECT * FROM Evaluations WHERE command='" + command + "'"
    db.cur.execute(execution_string)
    evals = db.cur.fetchall()

    print("%s was evaluated in %d out of %d total evals, that is %f" % (command, len(evals), ttl_num_evals, (float(len(evals))/ ttl_num_evals)))

    for eval in evals:
        eval_numb = eval[0]
        execution_string = "SELECT * FROM Reinforcements WHERE EvaluationId=" + str(eval_numb)
        db.cur.execute(execution_string)
        eval_reinforcements = db.cur.fetchall()
        print_data = False

        if (len(evals) > 25 and len(eval_reinforcements) > 2):
            print_data = True
        elif False: #len(evals) < 25:
            print_data = True
        if print_data:
            print("This eval recieved", len(eval_reinforcements), "reinforcements")
        for reinforcement in eval_reinforcements:
            if reinforcement[3] == 'n':
                numb_n += 1
            elif reinforcement[3] == 'y':
                # print(reinforcement)
                numb_y += 1
            else:
                print(reinforcement[3])
                exit()

    print("The command", command, "had", numb_y, "positive reinforcements and", numb_n, "negative reinforcements.")
