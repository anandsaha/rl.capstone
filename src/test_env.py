from environment import Environment
from robot import RobotArm
import time

def status(title, ra):
    print("")
    print(title)
    print("Is object held> ", ra.is_object_held())
    print("Is object in bin> ", ra.is_object_in_bin())
    print("------------------------>")

vrep_ip = '127.0.0.1'
vrep_port = 19997
#env = Environment(vrep_ip, vrep_port)

ra = RobotArm('127.0.0.1', 19997)
ra.restart_sim()

ra.set_object_location(-0.4, -0.02)
time.sleep(3)

ra.stop_sim()
ra.disconnect()
