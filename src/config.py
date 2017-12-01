"""
Configuration file to tune/adjust various parameters

(c) Anand Saha <anandsaha@gmail.com> 2017
"""

import utility

# Number of episodes to run
NUM_EPISODES = 10000
MIN_EPISODES_TO_RUN = 2500
# Number of max actions to execute per episode (terminate episode if this number is exceeded)
NUM_MAX_ACTIONS = 100
# Least actions needed to achieve the goal
MIN_ACTIONS_EXPECTED = 5

# Initial Q value to be populated for every state/action pair
Q_INIT_VAL = 0.0
# Epsilon value (the portion of exploratory actions)
EPSILON = 0.3
# The amount by which epsilon will be reduced every episode (to reduce exploration as we start executing more episodes)
EPSILON_DECAY = EPSILON * 0.0001
# The discount rate in equation of Q-Value
DISCOUNT = 0.8
# The learn rate in equation of Q-Value
LEARN_RATE = 0.5

Q_TABLE_DIR = 'qtables'
# File where Q table will be saved, loaded from. It's a numpy array.
Q_TABLE_FILE = 'qtables/qtable.txt.npy'
# File where per-episodic data will be saved: episode id, is success?, total rewards, total actions.
PLOT_FILE = 'qtables/episodes.txt'

# A filler state which represents an invalid state.
INVALID_STATE = [-100, -100, -100, False, -100, -100, -100]

# The step size to use to discretize the environment
UNIT_STEP_SIZE = 0.02
# A value to judge nearness
TOLERANCE = 0.01
# A finer value to judge nearness
TOLERANCE_FINER = 0.005

# Initial position of the arm (to be placed before any episode starts)
INIT_ARM_POSITION = [utility.rnd(-0.30), utility.rnd(-0.10), utility.rnd(0.14)]

# Dimension of the environment. [[xmin, xmax], [ymin, ymax], [zmin, zmax]]
ENV_DIMENSION = [[utility.rnd(-0.32), utility.rnd(-0.19)],
                 [utility.rnd(-0.12), utility.rnd(-0.05)],
                 [utility.rnd(0.00), utility.rnd(0.15)]]

# Some artificial delays to let V-REP stabilize after an action
SLEEP_VAL = 0.4
SLEEP_VAL_MIN = 0.3

# Distance between object and bin when object is in bin
CYLINDER_BIN_DISTANCE = 0.013

# Rewards
REWARD_TERMINATION = -10
REWARD_BAD_STEP = -3
REWARD_FIRST_SUCCESS = 5
REWARD_GOAL_ACHIEVED = 10
REWARD_DEFAULT = -1
