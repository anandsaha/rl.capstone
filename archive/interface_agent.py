from robot import RobotArm
import numpy as np
import copy
import os


class RobotArmAgent(object):
    """This class represents our agent. It carries out actions through the robot arm.
    The logic to calculate the reward and maintain the Q-Table also resides here."""

    def __init__(self, robot, alpha=0.1, gamma=0.9, epsilon=0.2, q_init=1):
        """Setup States, Actions and other initialization stuff"""

    def load_qtable(self, file):
        """Load the Q-Table from a file, called when starting a fresh run of episodes"""

    def store_qtable(self, file):
        """Store the Q-Table to a file, called when all episodes have ended"""

    def init(self):
        """Initialization stuff before beginning an episode"""

    def get_canonical_position(self, handle, claw_enabled):
        """Get the discrete position of an object specified by the handle.
        This represents state of the environment"""

    def update_actionstate(self, action_id):
        """Update action and state variables post an action."""

    def choose_action(self, state_id):
        """Choose an action given the state"""

    def execute_action(self, action_id):
        """Execute the given action"""

    def update_q_table(self, state, action, reward, state_new):
        """Update Q-Table"""

    def get_current_state(self):
        """Gets the current state of the environment"""

    def calculate_reward(self):
        """Calculate and return the reward post execution of an action"""

    def step_through(self):
        """Choose and Execute an action, calculate reward and update the Q-Table"""

    def main_loop(self, num_episodes):
        """Run as many episodes as specified in num_episodes"""

