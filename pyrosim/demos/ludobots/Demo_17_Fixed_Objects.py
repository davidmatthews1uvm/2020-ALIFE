import sys
sys.path.insert(0, '../..')

import pyrosim

sim = pyrosim.Simulator(eval_time=500)

ARM_LENGTH = 0.5
ARM_RADIUS = ARM_LENGTH / 10.0
cyl1 = sim.send_cylinder(x=0, y=0, z=ARM_LENGTH/2.0 + 2*ARM_RADIUS,
                   r1=0, r2=0, r3=1,
                   length=ARM_LENGTH, radius=ARM_RADIUS)
cyl2 = sim.send_cylinder(x=0, y=ARM_LENGTH/2.0,
                   z=ARM_LENGTH + 2 * ARM_RADIUS, r1=0, r2=1, r3=0,
                   length=ARM_LENGTH, radius=ARM_RADIUS)

# setting either first_body_id or second_body_id to -1 
# (pyrosim.Simulator.WORLD) will cause the joint to be attached 
# to the world at the defined point in space
joint1 = sim.send_hinge_joint(first_body_id=cyl1, second_body_id=cyl2,
                        x=0, y=0, z=ARM_LENGTH + 2*ARM_RADIUS,
                        n1=1, n2=0, n3=0,
                        lo=-3.14159/4.0, hi=+3.14159/4.0)
joint2 = sim.send_hinge_joint(first_body_id=cyl1,
                        second_body_id=pyrosim.Simulator.WORLD,
                        x=0, y=0,
                        z=ARM_LENGTH/2.0 + 2*ARM_RADIUS)
sim.start()
sim.wait_to_finish()
