import math
from kicker_pong.Constant import *


class Observation:

    def __init__(self):
        self._old_x_pos = 0
        self._old_y_pos = 0
        self._old_speed = 0
        self._old_angle = 0
        self._old_computer_gamer_pos = 0
        self._old_human_gamer_pos = 0
        self._state = []

    def update(self, kicker, ball, computer_gamer, human_gamer):
        standardize_x_pos = ball.get_x_position() / COURT_WIDTH
        standardize_y_pos = ball.get_y_position() / COURT_HEIGHT

        standardize_speed = ball.get_speed() / BALL_MAX_SPEED
        standardize_angle = ball.get_angle() / math.pi

        standardize_computer_gamer_pos = computer_gamer.get_position() / MAX_POS_KEEPER
        standardize_human_gamer_pos = human_gamer.get_position() / MAX_POS_KEEPER

        self._state = [kicker.get_score(), standardize_x_pos, self._old_x_pos,  standardize_y_pos, self._old_y_pos,
                       standardize_speed, self._old_speed, standardize_angle, self._old_angle,
                       standardize_computer_gamer_pos, self._old_computer_gamer_pos,
                       standardize_human_gamer_pos, self._old_human_gamer_pos]

        self._old_x_pos = standardize_x_pos
        self._old_y_pos = standardize_y_pos
        self._old_speed = standardize_speed
        self._old_angle = standardize_angle
        self._old_computer_gamer_pos = standardize_computer_gamer_pos
        self._old_human_gamer_pos = standardize_human_gamer_pos

        # new_x_pos = ball.get_x_position() + math.cos(ball.get_angle()) * ball.get_speed()
        # new_y_pos = ball.get_y_position() + math.sin(ball.get_angle()) * ball.get_speed()
        # self._state = [kicker.get_score(), ball.get_x_position(), ball.get_y_position(), new_x_pos, new_y_pos,
        #                computer_gamer.get_position()]

    def get_state(self):
        return self._state


class EnvironmentModel(Observation):

    def __init__(self):
        super().__init__()
        self.__reward = 0
        self.__old_score = [0, 0]
        self.__human_goal_counter = 0
        self.__done = False
        self.__enable_view = False

    def calc_reward(self, flag):
        # self.__reward += 0
        # if flag:
        #     self.__reward = 1
        if self.__done:
            score = self.get_state()[0][:]
            human_diff = score[0] - self.__old_score[0]
            computer_diff = score[1] - self.__old_score[1]
            if human_diff != 0:
                self.__reward = -1
            elif computer_diff != 0:
                self.__human_goal_counter += 1
                self.__reward = +1

            self.set_old_score(score)
        else:
            self.__reward = 0.01

    def get_reward(self):
        return self.__reward

    def set_reward(self, reward):
        self.__reward = reward

    def get_done(self):
        return self.__done

    def set_done(self, boolean):
        self.__done = boolean

    def set_enable_view(self, boolean):
        self.__enable_view = boolean

    def get_enable_view(self):
        return self.__enable_view

    def get_observation(self):
        return self.get_state()

    def set_old_score(self, score):
        self.__old_score = score

    def get_goal_counter(self):
        return self.__human_goal_counter

    def set_goal_counter(self, count):
        self.__human_goal_counter = count
