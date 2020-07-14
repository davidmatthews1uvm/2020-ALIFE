import sys
sys.path.insert(0, '../..')

import pyrosim

sim = pyrosim.Simulator()

sim.send_cylinder(x=0, y=0, z=0.5, r1=0, r2=1, r3=0)

sim.start()
sim.wait_to_finish()
