import numpy as np
import os
from utility import log_and_display
import config
from environment import Environment


class Agent(object):
    def __init__(self, env: Environment, epsilon, q_init_val, discount, learn_rate):

        self.env = env
        self.learn_rate = learn_rate
        self.discount = discount
        self.epsilon = epsilon

        self.q_table = np.full((env.total_states, env.total_actions), q_init_val)

        # Enable this to pre populate q table with known values - for faster convergence
        # self.pre_populate_qtable()

        self.current_state_id = None
        self.total_explorations = 0

    def pre_populate_qtable(self):
        """Not used, but can be invoked to pre-populate the Q table with good known values
        """
        log_and_display("Pre populating the Q Table with some known values - this helps in converging faster")
        for index, val in enumerate(self.q_table):
            if not self.env.states[index][3]:  # If object not held
                self.q_table[index][0] += config.REWARD_FIRST_SUCCESS  # Encourage grip enable
                self.q_table[index][1] -= config.REWARD_BAD_STEP
                if self.env.states[index][6] > 0.03:
                    for act in range(self.env.total_actions):
                        if self.env.actions[act][0] == self.env.action_type1 and self.env.actions[act][1][2] > 0.03:
                            self.q_table[index][act] = -100
            else:
                self.q_table[index][1] += config.REWARD_FIRST_SUCCESS
                self.q_table[index][0] -= config.REWARD_BAD_STEP
                if self.env.states[index][6] <= 0.07:
                    for act in range(self.env.total_actions):
                        if self.env.actions[act][0] == self.env.action_type1 and self.env.actions[act][1][2] <= 0.07:
                            self.q_table[index][act] = -100
        log_and_display("Done")

    def load_qtable(self):
        """The cached Q table is loaded before start of every episode
        """
        f = config.Q_TABLE_FILE
        if os.path.exists(f):
            self.q_table = np.load(f)

    def save_qtable(self):
        """The Q table is saved after every episode
        """
        f = config.Q_TABLE_FILE
        if os.path.exists(f):
            os.remove(f)
        np.save(f, self.q_table)

    def reset(self):
        """Prepares the Agent for a new episode.
        """
        log_and_display('Initializing episode')
        self.env.environment_reset()
        self.current_state_id = self.env.get_current_state()
        self.total_explorations = 0

    def select_action(self, current_state_id):
        """This method returns an action based on current state. It returns a mix of
        exploratory and exploitative actions based on epsilon value.
        """
        if np.random.uniform() < self.epsilon:
            log_and_display('Exploring...')
            self.total_explorations += 1
            action_id = np.random.choice(self.env.total_actions)
        else:
            log_and_display('Exploiting...')
            action_id = np.argmax(self.q_table[current_state_id])
        return action_id

    def execute_action(self, action_id):
        action = self.env.actions[action_id]

        if action[0] == self.env.action_type1:
            log_and_display('Action: Moving claw ' + str(action[1]))
            return self.env.move_arm(action[1], action_id)
        elif action[0] == self.env.action_type2:
            log_and_display('Action: Engaging/Disengaging claw ' + str(action[1]))
            return self.env.enable_grip(action[1], action_id)

    def update_q_table(self, state, action, reward, state_new):
        """Routing to update q-table.
        """
        q_current = self.q_table[state, action]
        error = reward + self.discount * np.max(self.q_table[state_new]) - q_current
        self.q_table[state, action] = q_current + self.learn_rate * error

        msg = "Q-Value: S:{}, A:{}, R:{}, S`:{}, TE: {}, Q:{}, Q`:{}".format(state, action, reward, state_new, error,
                                                                             q_current, self.q_table[state, action])
        log_and_display(msg)

    def execute_episode_qlearn(self, max_steps: int):
        """Invoking this method will execute one episode of training.
        """
        total_reward = 0
        total_steps = 0

        while max_steps > 0 and not self.env.is_goal_achieved() and not self.env.environment_breached:
            action_id = self.select_action(self.current_state_id)
            reward = self.execute_action(action_id)
            new_state_id = self.env.actionstate_curr['current_state_id']
            self.update_q_table(self.current_state_id, action_id, reward, new_state_id)
            self.current_state_id = new_state_id

            max_steps -= 1
            total_reward += reward
            total_steps += 1

        return total_reward, total_steps, self.env.is_goal_achieved(), self.total_explorations

    def execute_test(self, max_steps: int):
        """Here, assuming we have a robust qtable, we execute one episode which should succeed
        and the task should be accomplished.
        """
        total_reward = 0
        total_steps = 0
        self.epsilon = 0.0

        while max_steps > 0 and not self.env.is_goal_achieved() and not self.env.environment_breached:
            action_id = self.select_action(self.current_state_id)
            reward = self.execute_action(action_id)
            new_state_id = self.env.actionstate_curr['current_state_id']
            self.current_state_id = new_state_id

            max_steps -= 1
            total_reward += reward
            total_steps += 1

        return total_reward, total_steps, self.env.is_goal_achieved(), self.total_explorations


