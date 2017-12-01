# (C) Anand Saha <anandsaha@gmail.com>
# 23rd July 2017

import time
import vrep
import numpy as np
import utility
import config


class RobotArm(object):
    """Uses the V-REP remote client API to interact with the V-REP environment."""

    def __init__(self, ip, port):
        """Initializes connectivity to V-REP environment, initializes environmental variables.
        """
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart(ip, port, True, True, 5000, 5)
        if self.clientID != -1:
            print('Successfully connected to V-REP')
        else:
            raise RuntimeError('Could not connect to V-REP')

        # Some artificial delays to let V-REP stabilize after an action
        self.sleep_sec = config.SLEEP_VAL
        self.sleep_sec_min = config.SLEEP_VAL_MIN

        # id of the Robot Arm in V-REP environment
        self.main_object = 'uarm'
        # Initial state of the Gripper
        self.gripper_enabled = False

        # Get hands to various objects in the scene
        err, self.cylinder_handle = vrep.simxGetObjectHandle(self.clientID, 'uarm_pickupCylinder2',
                                                             vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("Could not get handle to the cylinder object. Halting program.")

        err, self.bin_handle = vrep.simxGetObjectHandle(self.clientID, 'uarm_bin',
                                                        vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("Could not get handle to the Bin object. Halting program.")

        err, self.gripper_handle = vrep.simxGetObjectHandle(self.clientID, 'uarmGripper_motor1Method2',
                                                            vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("Could not get handle to the Gripper object. Halting program.")

        # Distance between cylinder and bin when former is inside later
        # This was measured after putting the cylinder in the bin
        self.cylinder_bin_distance = config.CYLINDER_BIN_DISTANCE

        # Various values, to be set in the start_sim() function, because their values can be obtained
        # only after the simulation starts
        self.cylinder_height = None
        self.cylinder_z_locus = None
        self.bin_position = None
        self.objects = None
        self.object_positions = None

    def __del__(self):
        print('Disconnecting from V-REP')
        self.disconnect()

    def __update_all_object_positions(self):
        """Invokes API in V-REP environment to fetch position of all objects in the scene.
        """
        time.sleep(self.sleep_sec)
        err, handles, ints, floats, strings = vrep.simxGetObjectGroupData(self.clientID,
                                                                          vrep.sim_appobj_object_type, 3,
                                                                          vrep.simx_opmode_blocking)

        positions = np.array(floats)
        self.objects = handles
        self.object_positions = positions.reshape(len(handles), 3)

    def disconnect(self):
        self.stop_sim()
        vrep.simxGetPingTime(self.clientID)
        vrep.simxFinish(self.clientID)

    def get_position(self, handle):
        """Uses the cached positions to return position of any given object handle
        """
        # self.object_positions is updated by the __update_all_object_positions() method
        pos = self.object_positions[self.objects.index(handle)].tolist()
        for idx, val in enumerate(pos):
            pos[idx] = utility.rnd(pos[idx])
        return pos

    @staticmethod
    def get_env_dimensions():
        # Dimensions of the virtual space within which the arm should maneuver
        # X min, max; Y min, max; Z min, max
        dim = config.ENV_DIMENSION
        return dim

    def goto_position(self, pos):
        """Maneuvers the robotic arm to the given position.
        """
        time.sleep(self.sleep_sec)

        pos_adjusted = list(pos)
        pos_adjusted.append(0.0)  # Required by V-REP
        pos_adjusted.append(0.0)  # Required by V-REP

        err, retInts, retFloats, retStrings, retBuff = vrep.simxCallScriptFunction(self.clientID,
                                                                                   self.main_object,
                                                                                   vrep.sim_scripttype_childscript,
                                                                                   'computeAnglesFromGripperPositionEx',
                                                                                   [], pos_adjusted, [], bytearray(),
                                                                                   vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("goto_position(): Failed to compute angles")

        err, retInts, retFloats, retStrings, retBuff = vrep.simxCallScriptFunction(self.clientID,
                                                                                   self.main_object,
                                                                                   vrep.sim_scripttype_childscript,
                                                                                   'moveToPositionEx',
                                                                                   [], retFloats, [], bytearray(),
                                                                                   vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("goto_position(): Failed to move the arm")

        # Since we have moved the arm, we need to take stock of positions of all the objects
        self.__update_all_object_positions()

    def enable_grip(self, enable):
        """Engages/Disengages the gripper.
        """
        time.sleep(self.sleep_sec_min)

        i_enable = 1
        if not enable:
            i_enable = -1

        err, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(self.clientID,
                                                                                     self.main_object,
                                                                                     vrep.sim_scripttype_childscript,
                                                                                     'enableGripperEx',
                                                                                     [i_enable], [], [], bytearray(),
                                                                                     vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("enable_grip(): Failed to enable/disable grip")

        # Since we have altered the grip, we need to take stock of positions of all the objects
        self.__update_all_object_positions()
        self.gripper_enabled = enable

    def start_sim(self):
        time.sleep(self.sleep_sec_min)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
        self.gripper_enabled = False
        self.__update_all_object_positions()
        self.cylinder_height = self.get_object_height(self.cylinder_handle)
        self.cylinder_z_locus = self.get_position(self.cylinder_handle)[2]
        self.bin_position = self.get_position(self.bin_handle)

    def stop_sim(self):
        time.sleep(self.sleep_sec_min)
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)

    def restart_sim(self):
        self.stop_sim()
        self.start_sim()

    def get_object_height(self, handle):
        time.sleep(self.sleep_sec_min)
        err, minval = vrep.simxGetObjectFloatParameter(self.clientID,
                                                       handle, vrep.sim_objfloatparam_modelbbox_min_z,
                                                       vrep.simx_opmode_blocking)

        if err != vrep.simx_return_ok:
            raise RuntimeError("get_object_height(): Failed to get parameters: sim_objfloatparam_modelbbox_min_z")

        err, maxval = vrep.simxGetObjectFloatParameter(self.clientID,
                                                       handle, vrep.sim_objfloatparam_modelbbox_max_z,
                                                       vrep.simx_opmode_blocking)
        if err != vrep.simx_return_ok:
            raise RuntimeError("get_object_height(): Failed to get parameters: sim_objfloatparam_modelbbox_max_z")

        return maxval - minval

    def is_object_held(self):
        """Based on position of the gripper and object, calculates if the object is being held by the gripper.
        """
        pos_cylinder = self.get_position(self.cylinder_handle)
        pos_gripper = self.get_position(self.gripper_handle)

        x = np.abs(pos_cylinder[0] - pos_gripper[0])
        y = np.abs(pos_cylinder[1] - pos_gripper[1])
        z = np.abs(pos_cylinder[2] - pos_gripper[2])

        if x <= 0.01 and y == 0.0 and z <= 0.02 and self.gripper_enabled:
            return True

        return False

    def is_object_in_bin(self):
        """Based on position of the bin and the object, calculates if the object is being held by the gripper.
        """
        pos_bin = self.get_position(self.bin_handle)
        pos_cyl = self.get_position(self.cylinder_handle)

        return utility.distance(pos_bin, pos_cyl) < self.cylinder_bin_distance

