# (C) Anand Saha <anandsaha@gmail.com>
# 23rd July 2017

import time
import vrep
import numpy as np


class RobotArm(object):
    """This represents the Robot Arm. It makes use of the V-REP remote client library
    to interface with the virtual robot arm in V-REP environment. Among other things, this
    class can get positions of objects, command the arm to move to a given location and
    grab an object."""

    def __init__(self, ip, port):
    """Initialise the Robot"""

    def __del__(self):
        """Call disconnect()"""

    def disconnect(self):
        """Stop the simulation and disconnect from V-REP environment"""

    def get_position(self, handle):
        """Get position of the object represented by the handle passed"""

    @staticmethod
    def get_env_dimensions():
        """Get dimensions of the environment (x, y, z positions of length vs breath vs height)
           The gripper can go to any location within this environment.
        """

    def goto_position(self, pos):
        """Make the robot arm gripper go to the specified position (x, y z coordinates)"""

    def enable_gripper(self, enable):
        """Enable the gripper"""

    def get_gripper_status(self, mode):
        """Check if gripper is engaged or relaxed"""

    def start_sim(self):
        """Start the simulation"""

    def stop_sim(self):
        """Stop the simulation"""

    def restart_sim(self):
        """Restart the simulation. i.e. Stop followed by Start"""

    def get_object_height(self, handle):
        """Get the bounding box height of an object specified by the handle passed"""

    def is_object_held(self):
        """Is the object (cylinder) held by the gripper? Return True/False"""

    def is_object_in_bin(self):
        """Is the object (cylinder) in the bin? Return True/False"""

    def update_all_object_positions(self):
        """Retrieve and store all positions (x, y z coordinates) of all the objects in the scene"""
