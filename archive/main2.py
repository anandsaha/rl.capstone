from robot import RobotArm
import numpy as np 
import time
import vrep
import utility
from decimal import Decimal

def distance(pos1, pos2):
    x2 = np.square(pos1[0] - pos2[0])
    y2 = np.square(pos1[1] - pos2[1])
    z2 = np.square(pos1[2] - pos2[2])
    return np.sqrt(x2 + y2 + z2)

def status(title, ra):
    print("")
    print(title)
    print("Is object held> ", ra.is_object_held())
    print("Is object in bin> ", ra.is_object_in_bin())
    print("------------------------>")

ra = RobotArm('127.0.0.1', 19997)
ra.restart_sim()


ra.goto_position([Decimal('-0.30'), Decimal('-0.10'), Decimal('0.04')])
status("", ra)

ra.enable_grip(True)
status("", ra)


ra.goto_position([Decimal('-0.30'), Decimal('-0.10'), Decimal('0.04')])
status("", ra)


ra.goto_position([Decimal('-0.30'), Decimal('-0.10'), Decimal('0.06')])
status("", ra)


ra.goto_position([Decimal('-0.24'), Decimal('-0.10'), Decimal('0.12')])
status("", ra)


ra.enable_grip(False)
status("", ra)

ra.goto_position([Decimal('-0.26'), Decimal('-0.10'), Decimal('0.10')])
status("", ra)

quit()

pos = ra.get_position(ra.cylinder_handle)
status("After getting position of cylinder", ra)

pos[0] += utility.rnd(0.0)

ra.goto_position(pos)
status("After going to the cylinder", ra)

ra.enable_grip(True)
status("After enabling grip", ra)

pos = ra.get_position(ra.cylinder_handle)
status("After fetching position", ra)

pos[2] *= 6 
ra.goto_position(pos)
status("After lifting", ra)

pos = ra.get_position(ra.bin_handle)
status("After getting position of bin", ra)

pos[2] *= 4
ra.goto_position(pos)
status("After going to bin top", ra)

ra.enable_grip(False)
status("After releasing", ra)

"""
#ra.get_gripper_status(vrep.simx_opmode_streaming)
#ra.get_gripper_status(vrep.simx_opmode_buffer)
ra.goto_position([-0.17, -0.09, 0.25])
time.sleep(5)

ra.enable_grip(False)
pos = ra.get_position(ra.cylinder_handle)
ra.goto_position(pos)
ra.enable_grip(True)
pos[2] *= 5 
ra.goto_position(pos)
ra.goto_position(ra.bin_position) 
ra.enable_grip(False)

i = 0
dim = ra.get_env_dimensions()

while i < 100:
    x = np.arange(dim[0][0], dim[0][1], 0.002)
    y = np.arange(dim[1][0], dim[1][1], 0.002)
    z = np.arange(dim[2][0], dim[2][1], 0.002)

    ra.goto_position([np.random.choice(x), np.random.choice(y), np.random.choice(z)])

    i += 1
"""


ra.stop_sim()
ra.disconnect()

