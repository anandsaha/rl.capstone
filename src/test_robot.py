from robot import RobotArm
import numpy as np 
import utility
import config


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

pos = ra.get_position(ra.cylinder_handle)
status("After getting position of cylinder", ra)

pos[0] += utility.rnd(0.0)

ra.goto_position(pos)
status("After going to the cylinder", ra)

ra.enable_grip(True)
status("After enabling grip", ra)

pos = ra.get_position(ra.cylinder_handle)
status("After fetching position", ra)

pos[2] = utility.rnd(0.10) 
ra.goto_position(pos)
status("After lifting", ra)

pos = ra.get_position(ra.bin_handle)
status("After getting position of bin", ra)

pos[2] = utility.rnd(0.10)  
ra.goto_position(pos)
status("After going to bin top", ra)

ra.enable_grip(False)
status("After releasing", ra)

dist = utility.distance(ra.bin_position, ra.get_position(ra.bin_handle))
print(dist)
if dist > config.TOLERANCE:
    print("Bin is not in position")
else:
    print("Bin is in position")

print("Reset ==================================================")

ra.restart_sim()
pos = ra.get_position(ra.cylinder_handle)
print(pos)
ra.goto_position(pos)
pos = ra.get_position(ra.cylinder_handle)
print(pos)


"""
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
"""

ra.stop_sim()
ra.disconnect()

