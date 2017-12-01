from utility import log_and_display
import utility
import config


def is_valid_state(env):
    if env.actionstate_curr['state'] == env.invalid_state:
        return False
    return True


def is_cylinder_standing(env):
    cylinder_pos = env.robot.get_position(env.robot.cylinder_handle)
    if (cylinder_pos[2] - env.robot.cylinder_z_locus) <= (-1 * config.TOLERANCE_FINER):
        return False
    return True


def is_bin_inplace(env):
    if utility.distance(env.robot.bin_position, env.actionstate_curr['bin_position']) > config.TOLERANCE_FINER:
        return False
    return True


def is_previous_current_state_same(env):
    if len(env.actionstate_prev) > 0 and env.actionstate_curr['state'] == env.actionstate_prev['state']:
        return True
    return False


def is_grip_engaged_with_no_object(env):
    if env.robot.gripper_enabled \
            and not env.actionstate_curr['is_cylinder_held'] \
            and not env.actionstate_curr['cylinder_in_bin']:
        return True
    return False


def is_cylinder_not_dropped_in_bin(env):
    if len(env.actionstate_prev) > 0 \
            and env.actionstate_prev['is_cylinder_held'] \
            and not env.actionstate_curr['is_cylinder_held'] \
            and not env.actionstate_curr['cylinder_in_bin']:
        return True
    return False


def is_grip_holding_object(env):
    if not env.episode_object_gripped \
            and env.robot.gripper_enabled \
            and env.actionstate_curr['is_cylinder_held'] \
            and not env.actionstate_curr['cylinder_in_bin']:
        env.episode_object_gripped = True
        return True
    return False


def is_object_in_bin(env):
    if len(env.actionstate_prev) > 0 \
            and env.actionstate_prev['is_cylinder_held'] \
            and env.actionstate_curr['cylinder_in_bin'] \
            and is_cylinder_standing(env)\
            and not is_grip_holding_object(env) \
            and is_bin_inplace(env):
        return True
    return False


def calculate_reward(env):
    """Implements the reward strategy, returns reward, environment_breached, is_success
    """

    if not is_valid_state(env):
        log_and_display('Penalty: Reached invalid state, terminating')
        return config.REWARD_TERMINATION, True, False

    if not is_cylinder_standing(env):
        log_and_display('Penalty: Cylinder has fallen, terminating')
        return config.REWARD_TERMINATION, True, False

    if not is_bin_inplace(env):
        log_and_display('Penalty: Bin has shifted, terminating')
        return config.REWARD_TERMINATION, True, False

    if is_grip_engaged_with_no_object(env):
        log_and_display('Penalty: Claw is engaged but cylinder is not in claw')
        return config.REWARD_BAD_STEP, False, False

    if is_cylinder_not_dropped_in_bin(env):
        log_and_display('Penalty: Claw did not drop the cylinder in the bin')
        return config.REWARD_BAD_STEP, False, False

    if is_grip_holding_object(env):
        log_and_display('Reward: Claw could grab the cylinder for first time')
        return config.REWARD_FIRST_SUCCESS, False, False

    if is_object_in_bin(env):
        log_and_display('Reward: Cylinder in bucket. Objective achieved !!!!!!!!')
        return config.REWARD_GOAL_ACHIEVED, True, True

    return config.REWARD_DEFAULT, False, False  # Default
