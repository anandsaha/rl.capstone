from robot import RobotArm
import numpy as np 

ra = RobotArm('127.0.0.1', 19997)

ra.restart_sim()

posc = ra.get_position(ra.cylinder_handle)
posb = ra.get_position(ra.bin_handle)

x1 = posb[0]
x2 = posc[0]
if posc[0] < posb[0]:
    x1 = posc[0]
    x2 = posb[0]

y1 = posb[1]
y2 = posc[1]
if posc[1] < posb[1]:
    y1 = posc[1]
    y2 = posb[1]


z1 = posb[2]
z2 = posc[2]
if posc[2] < posb[2]:
    z1 = posc[2]
    z2 = posb[2]


print('[[{}, {}], [{}, {}], [{}, {}]]'.format(round(x1 - 0.02, 2), round(x2 + 0.02, 2), 
            round(y1 - 0.02, 2), round(y2 + 0.02, 2), 0, round(z2, 2) * 4))

ra.stop_sim()
ra.disconnect()
