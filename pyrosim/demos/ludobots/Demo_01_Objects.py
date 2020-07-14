import sys
sys.path.insert(0, '../..')

import pyrosim

sim = pyrosim.Simulator(play_paused=True)

sim.send_cylinder()

sim.start()
sim.wait_to_finish()
