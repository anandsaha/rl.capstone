from robot import RobotArm
import numpy as np 
import time
import vrep
import decimal
import utility
import decimal


def status(title, ra):
    print("")
    print(title)
    print("Is object held> ", ra.is_object_held())
    print("Is object in bin> ", ra.is_object_in_bin())
    print("------------------------>")

ra = RobotArm('127.0.0.1', 19997)
ra.restart_sim()

pos = ra.get_position(ra.cylinder_handle)
pos[2] += utility.rnd(0.02)
ra.goto_position(pos)
status("", ra)
time.sleep(2)
ra.enable_grip(True)
status("", ra)
time.sleep(2)
pos[2] *= 6
ra.goto_position(pos)
time.sleep(2)

"""
print(ra.get_env_dimensions())
pos = ra.get_position(ra.gripper_handle)
print(pos)
pos[0] += utility.rnd(0.01)
pos[1] += utility.rnd(0.01)
pos[2] += utility.rnd(0.01)
print(pos)
ra.goto_position(pos)
pos = ra.get_position(ra.gripper_handle)
print(pos)
"""
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

