import sqlite3
import numpy as np
import pickle


database_file = "../data/database.db"
ignore_list_file = "ignore_list.txt"

def Command_Stats(curr):
    print("Command Stats...")
    # get list of ignore_listed commands.
    ignore_list = set(line.strip() for line in open(ignore_list_file, "r").readlines())

    curr.execute("SELECT command, commandEncoding FROM UniqueCommands")
    commands_raw = curr.fetchall()
    num_commands = len(commands_raw)

    commands = sorted([(len(cmd.split(' ')), cmd.split(' '), cmd, np.mean(pickle.loads(cmd_raw), axis=0), pickle.loads(cmd_raw)) for cmd, cmd_raw in commands_raw if cmd not in ignore_list])
    commands_len_1 = [cmd for cmd in commands if cmd[0] == 1]

    print("Unique commands: %d"%len(commands))
    print("Unique commands of length 1: %d"%len(commands_len_1))

    NUM_TOP_COMMANDS = 5
    curr.execute(
        "Select e.command, COUNT(e.command) from Reinforcements r JOIN Evaluations e on r.EvaluationId = e.Id JOIN Evaluations e2 on e.Date = e2.date Where e.Id < e2.Id GROUP BY e.command ORDER BY COUNT(e.command) DESC limit ?",
        (NUM_TOP_COMMANDS,))
    top_commands = [(cmd, rank, reinforcement_count) for rank, (cmd, reinforcement_count) in enumerate(curr.fetchall()) if
                    len(cmd.split(' ')) == 1 and cmd not in ignore_list]
    print("Top %d most popular commands:" %(NUM_TOP_COMMANDS))
    for cmd, rank, count in top_commands:
        print("    * (%d) '%s' was sent %d times"%(rank, cmd,  count))

    print("\n")


def Subject_Stats(curr):
    print("Subject Stats...")
    curr.execute("SELECT * from Users")
    users = curr.fetchall()
    num_users = len(users)
    print("Subjects in total: %d" % num_users)

    curr.execute("SELECT u1.Id, count(u1.Id) From Users u1 JOIN Reinforcements r1 on u1.Id = r1.UserId JOIN Reinforcements r2 on r1.Date = r2.Date where r1.Id < r2.Id GROUP BY u1.Id ORDER BY COUNT(u1.Id)")

    evals_per_user_raw = np.array(curr.fetchall())
    evals_per_user = evals_per_user_raw[:, 1]

    mean_evals_per_user = np.mean(evals_per_user)
    std_evals_per_user = np.std(evals_per_user)
    median_evals_per_user = np.median(evals_per_user)

    print("Subjects sending reinforcments: %d"%len(evals_per_user))
    print("Reinforcement signals per subject: mean: %.2f (std: %.2f) median: %.2f" %(mean_evals_per_user, std_evals_per_user, median_evals_per_user))
    print("Reinforcement signals per subject: min: %.2f max: %.2f" %(np.min(evals_per_user), np.max(evals_per_user)))
    print("\n")


def Robot_Stats(curr):
    print("Robot Stats...")
    curr.execute("SELECT * From Robots")
    robots = curr.fetchall()
    num_robots = len(robots)
    print("Robots in total: %d" % num_robots)

    curr.execute("Select * From Evaluations e1 JOIN Evaluations e2 on e1.Date = e2.Date where e1.Id < e2.Id")
    evals = curr.fetchall()
    num_evals = evals[-1][0]/2
    evals_reinforced = len(evals)
    print("Total evals shown: %d" %num_evals)
    print("Total evals reinforced: %d" %evals_reinforced)
    print("Percent of evals reinforced: %.2f%%" %(100 * evals_reinforced/num_evals ))

    print("\n")


def Reinforcements_Stats(curr):
    print("Reinforcement Stats...")
    curr.execute("SELECT * FROM Reinforcements")
    reinforcements  = curr.fetchall()
    num_reinforcements = len(reinforcements) / 2
    print("There are %d reinforcements in total." % num_reinforcements)
    print("\n")


def Chat_Stats(curr):
    print("Chat Stats...")
    curr.execute("SELECT count(*) from ChatEntries")
    print("Total chat messages: %d"%curr.fetchone())

# users, Robots, commands, reinforcements.

if __name__ == '__main__':

    # connect to the database + extract out relavent data to test if evolution is occuring.
    conn = sqlite3.connect(database_file)
    curr = conn.cursor()

    Subject_Stats(curr)
    Command_Stats(curr)
    Robot_Stats(curr)
    Reinforcements_Stats(curr)

    Chat_Stats(curr)


