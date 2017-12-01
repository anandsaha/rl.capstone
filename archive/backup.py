def calculate_reward(self):
    state_new = self.actionstate_curr['state']

    terminate = False
    is_pass = False

    if state_new == self.invalid_state:
        reward = float('-inf')
        log_and_display('Penalty: Reached invalid state, terminating')
        terminate = True
    elif (ra.get_position(ra.cylinder_handle)[2] - ra.cylinder_z_locus) <= (-1 * self.tolerance):
        reward = float('-inf')
        log_and_display('Penalty: Cylinder has fallen, terminating')
        terminate = True
    elif utility.distance(ra.bin_position, self.actionstate_curr['bin_position']) > self.tolerance:
        reward = float('-inf')
        log_and_display('Penalty: Bin has shifted, terminating')
        terminate = True
    elif len(self.actionstate_prev) > 0 and self.actionstate_curr['state'] == self.actionstate_prev['state']:
        reward = float('-inf')
        log_and_display('Penalty: Previous and current state is same')
    elif self.robot.gripper_enabled \
            and not self.actionstate_curr['is_cylinder_held'] \
            and not self.actionstate_curr['cylinder_in_bin']:
        reward = float('-inf')
        log_and_display('Penalty: Claw is engaged but cylinder is not in claw')
    elif len(self.actionstate_prev) > 0 \
            and self.actionstate_prev['is_cylinder_held'] \
            and not self.actionstate_curr['is_cylinder_held'] \
            and not self.actionstate_curr['cylinder_in_bin']:
        reward = float('-inf')
        log_and_display('Penalty: Claw did not drop the cylinder in the bin')
    elif not self.episode_object_gripped and self.robot.gripper_enabled \
            and self.actionstate_curr['is_cylinder_held'] \
            and not self.actionstate_curr['cylinder_in_bin']:
        self.episode_object_gripped = True
        reward = 50
        log_and_display('Reward: Claw could grab the cylinder for first time !!!!!!!!!!!!!!!!!!!!!!!!!')
        """
        if (ra.get_position(ra.cylinder_handle)[2] - ra.cylinder_z_locus) > self.tolerance:
            reward = 10
            log_and_display('Reward: Claw could grab *and lift* the cylinder !!!!!!!!!!!!!!!!!!!!!!!!!')
        else:
            reward = 5
            log_and_display('Reward: Claw could grab the cylinder !!!!!!!!!!!!!!!!!!!!!!!!!')
        """
    elif self.actionstate_curr['cylinder_in_bin']:
        reward = 100
        log_and_display('Reward: Cylinder in bucket !!!!!!!!!!!!!!!!!!!!!!!!!')
        terminate = True
        is_pass = True
    else:
        reward = float('-inf')

    return reward, terminate, is_pass