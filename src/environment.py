import numpy as np
import utility
import copy
from utility import log_and_display
from robot import RobotArm
import reward_strategy
import config


class Environment(object):

    def __init__(self, vrep_ip: str, vrep_port: int):
        """Prepares the actions, states and other environment variables
        """
        self.robot = RobotArm(vrep_ip, vrep_port)

        self.tolerance = utility.rnd(config.TOLERANCE)
        self.unit_step = utility.rnd(config.UNIT_STEP_SIZE)

        dim = self.robot.get_env_dimensions()

        # Actions #########################################################
        # The actions the agent can take - either goto some x,y,z position
        # or engage/disengage claw

        x_range_actions = np.arange(dim[0][0], dim[0][1], self.unit_step)
        y_range_actions = np.arange(dim[1][0], dim[1][1], self.unit_step)
        z_range_actions = np.arange(dim[2][0], dim[2][1], self.unit_step)

        # Actions consist of
        #   a) Gripper Enable/Disable
        #   b) Goto location (x, y, z)
        self.action_type1 = 'move_gripper'
        self.action_type2 = 'engage_gripper'
        self.actions = []
        self.actions.append([self.action_type2, True])
        self.actions.append([self.action_type2, False])

        print(x_range_actions[1:-1])
        print(y_range_actions[1:-1])
        print(z_range_actions[1:-1])

        for x in x_range_actions[1:-1]:
            for y in y_range_actions[1:-1]:
                for z in z_range_actions[1:-1]:
                    self.actions.append([self.action_type1, [x, y, z]])

        self.total_actions = len(self.actions)

        # States #########################################################
        # States consist of
        #   a) Position of the object (x, y, z coordinates)
        #   b) If it is held by gripper or not
        #   c) Position of the gripper (x, y, z coordinates)
        x_range = np.arange(dim[0][0], dim[0][1], self.tolerance)
        y_range = np.arange(dim[1][0], dim[1][1], self.tolerance)
        z_range = np.arange(dim[2][0], dim[2][1], self.tolerance)

        self.states = []
        self.invalid_state = config.INVALID_STATE
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    for b in [True, False]:
                        for xa in x_range_actions:
                            for ya in y_range_actions:
                                for za in z_range_actions:
                                    self.states.append([x, y, z, b, xa, ya, za])

        # invalid state, the last state. This state suggests that the object is outside the environment.
        self.states.append(self.invalid_state)
        self.total_states = len(self.states)
        self.invalid_states_index = self.total_states - 1

        log_and_display("There are {0} actions.".format(self.total_actions))
        log_and_display("There are {0} states.".format(self.total_states))

        self.episode_object_gripped = False
        self.environment_breached = False
        self.is_success = False
        self.actionstate_prev = {}
        self.actionstate_curr = {}

    def environment_reset(self):
        """Prepares the Environment for a new episode.
        """
        self.robot.restart_sim()
        self.robot.goto_position(config.INIT_ARM_POSITION)
        self.episode_object_gripped = False
        self.environment_breached = False
        self.is_success = False
        self.actionstate_prev = {}
        self.actionstate_curr = {}

    def __get_canonical_state(self):
        """Fetches position of the arm, the object and state of the gripper, calculates the state id that
        their values correspond to, and returns the state id
        """
        pos_obj = self.robot.get_position(self.robot.cylinder_handle)
        pos_arm = self.robot.get_position(self.robot.gripper_handle)
        object_held = self.robot.is_object_held()

        current_state_id = 0
        for state in self.states:
            if abs(state[0] - pos_obj[0]) < self.tolerance \
                    and abs(state[1] - pos_obj[1]) < self.tolerance \
                    and abs(state[2] - pos_obj[2]) < self.tolerance \
                    and state[3] == object_held \
                    and abs(state[4] - pos_arm[0]) < self.unit_step \
                    and abs(state[5] - pos_arm[1]) < self.unit_step \
                    and abs(state[6] - pos_arm[2]) < self.unit_step:
                return current_state_id
            current_state_id += 1

        log_and_display('State was invalid: ' + str(pos_obj) + str(object_held) + str(pos_arm))
        return self.invalid_states_index

    def __update_actionstate(self, action_id):
        """Caches various environment parameters. Used for reward calculation among other things.
        """
        self.actionstate_curr['action_id'] = action_id
        self.actionstate_curr['current_state_id'] = self.get_current_state()
        self.actionstate_curr['state'] = self.states[self.actionstate_curr['current_state_id']]
        self.actionstate_curr['cylinder_position'] = self.get_object_position()
        self.actionstate_curr['bin_position'] = self.get_destination_position()
        self.actionstate_curr['claw_position'] = self.get_arm_position()

        self.actionstate_curr['claw_cylinder_distance'] = utility.distance(self.actionstate_curr['claw_position'],
                                                                           self.actionstate_curr['cylinder_position'])
        self.actionstate_curr['bin_cylinder_distance'] = utility.distance(self.actionstate_curr['bin_position'],
                                                                          self.actionstate_curr['cylinder_position'])
        self.actionstate_curr['cylinder_in_bin'] = self.robot.is_object_in_bin()
        self.actionstate_curr['is_cylinder_held'] = self.robot.is_object_held()

    def get_current_state(self):
        return self.__get_canonical_state()

    def get_arm_position(self):
        return self.robot.get_position(self.robot.gripper_handle)

    def get_object_position(self):
        return self.robot.get_position(self.robot.cylinder_handle)

    def get_destination_position(self):
        return self.robot.get_position(self.robot.bin_handle)

    def move_arm(self, position: list, action_id: int):
        self.actionstate_prev = copy.deepcopy(self.actionstate_curr)
        self.robot.goto_position(position)
        self.__update_actionstate(action_id)
        reward, breached, is_success = reward_strategy.calculate_reward(self)
        self.environment_breached = breached
        self.is_success = is_success
        return reward

    def enable_grip(self, enable: bool, action_id: int):
        self.actionstate_prev = copy.deepcopy(self.actionstate_curr)
        self.robot.enable_grip(enable)
        self.__update_actionstate(action_id)
        reward, breached, is_success = reward_strategy.calculate_reward(self)
        self.environment_breached = breached
        self.is_success = is_success
        return reward

    def is_goal_achieved(self):
        return self.is_success
