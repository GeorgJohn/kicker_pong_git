import math
from kicker_pong.Constant import *


class Kicker:
    def __init__(self, time_delta):
        self.__borderline_x_min = BALL_RADIUS
        self.__borderline_x_max = COURT_WIDTH - BALL_RADIUS
        self.__borderline_y_min = BALL_RADIUS
        self.__borderline_y_max = COURT_HEIGHT - BALL_RADIUS
        self.__borderline_goal_bar_y_min = GOAL_BAR_POS + BALL_RADIUS
        self.__borderline_goal_bar_y_max = GOAL_BAR_POS + GOAL_SIZE - BALL_RADIUS
        self.__goal_line_human = COURT_WIDTH + BALL_RADIUS
        self.__goal_line_computer = - BALL_RADIUS
        self.__time = time_delta
        self.__ball_in_goal_area = False
        self.__score = [0, 0]

    def collision(self, ball):
        new_pos_in_range = False
        if not self.__ball_in_goal_area:
            if ball.get_new_x_position() > self.__borderline_x_max:
                if self.__borderline_goal_bar_y_min < ball.get_new_y_position() < self.__borderline_goal_bar_y_max:
                    x_pos_in_range = True
                    self.__ball_in_goal_area = True
                else:
                    delta_t_collision = (self.__borderline_x_max - ball.get_x_position()) / \
                                        (math.cos(ball.get_angle()) * ball.get_speed())
                    if ball.get_angle() < 0:
                        ball.set_new_angle(- math.pi - ball.get_angle())
                    elif ball.get_angle() > 0:
                        ball.set_new_angle(math.pi - ball.get_angle())
                    ball.set_new_y_position(ball.get_y_position() +
                                            math.sin(ball.get_angle()) * ball.get_speed() * self.__time)
                    ball.set_new_x_position(self.__borderline_x_max +
                                            math.cos(ball.get_new_angle()) *
                                            ball.get_speed() * (self.__time - delta_t_collision))
                    x_pos_in_range = False
            elif ball.get_new_x_position() < self.__borderline_x_min:
                if self.__borderline_goal_bar_y_min < ball.get_new_y_position() < self.__borderline_goal_bar_y_max:
                    x_pos_in_range = True
                    self.__ball_in_goal_area = True
                else:
                    delta_t_collision = (self.__borderline_x_min - ball.get_x_position()) / \
                                        (math.cos(ball.get_angle()) * ball.get_speed())
                    if ball.get_angle() < 0:
                        ball.set_new_angle(- math.pi - ball.get_angle())
                    elif ball.get_angle() > 0:
                        ball.set_new_angle(math.pi - ball.get_angle())
                    else:
                        ball.set_new_angle(0)
                    ball.set_new_y_position(ball.get_y_position() +
                                            math.sin(ball.get_angle()) * ball.get_speed() * self.__time)
                    ball.set_new_x_position(self.__borderline_x_min +
                                            math.cos(ball.get_new_angle()) *
                                            ball.get_speed() * (self.__time - delta_t_collision))
                    x_pos_in_range = False
            else:
                x_pos_in_range = True

            if ball.get_new_y_position() > self.__borderline_y_max:
                delta_t_collision = (self.__borderline_y_max - ball.get_y_position()) / \
                                    (math.sin(ball.get_angle()) * ball.get_speed())
                ball.set_new_angle(- ball.get_angle())
                ball.set_new_x_position(ball.get_x_position() +
                                        math.cos(ball.get_angle()) * ball.get_speed() * self.__time)
                ball.set_new_y_position(self.__borderline_y_max +
                                        math.sin(ball.get_new_angle()) *
                                        ball.get_speed() * (self.__time - delta_t_collision))
                y_pos_in_range = False
            elif ball.get_new_y_position() < self.__borderline_y_min:
                delta_t_collision = (ball.get_y_position() - self.__borderline_y_min) / \
                                    (math.sin(ball.get_angle()) * ball.get_speed())
                ball.set_new_angle(- ball.get_angle())
                ball.set_new_x_position(ball.get_x_position() +
                                        math.cos(ball.get_angle()) * ball.get_speed() * self.__time)
                ball.set_new_y_position(self.__borderline_y_min +
                                        math.sin(ball.get_new_angle()) *
                                        ball.get_speed() * (self.__time - delta_t_collision))
                y_pos_in_range = False
            else:
                y_pos_in_range = True
        else:
            if ball.get_new_x_position() > self.__goal_line_human:
                self.score_counter(Gamer.COMPUTER)
                ball.set_terminal(True)
                self.__ball_in_goal_area = False
            elif ball.get_new_x_position() < self.__goal_line_computer:
                self.score_counter(Gamer.HUMAN)
                ball.set_terminal(True)
                self.__ball_in_goal_area = False
            else:
                if ball.get_new_y_position() > self.__borderline_goal_bar_y_max:
                    delta_t_collision = (self.__borderline_goal_bar_y_max - ball.get_y_position())\
                                        / (math.sin(ball.get_angle()) * ball.get_speed())
                    ball.set_new_angle(- ball.get_angle())
                    ball.set_new_x_position(ball.get_x_position() +
                                            math.cos(ball.get_angle()) * ball.get_speed() * self.__time)
                    ball.set_new_y_position(self.__borderline_goal_bar_y_max +
                                            math.sin(ball.get_new_angle()) *
                                            ball.get_speed() * (self.__time - delta_t_collision))
                elif ball.get_new_y_position() < self.__borderline_goal_bar_y_min:
                    delta_t_collision = (ball.get_y_position() - self.__borderline_goal_bar_y_min)\
                                        / (math.sin(ball.get_angle()) * ball.get_speed())
                    ball.set_new_angle(- ball.get_angle())
                    ball.set_new_x_position(ball.get_x_position() +
                                            math.cos(ball.get_angle()) * ball.get_speed() * self.__time)
                    ball.set_new_y_position(self.__borderline_goal_bar_y_min +
                                            math.sin(ball.get_new_angle()) *
                                            ball.get_speed() * (self.__time - delta_t_collision))
            y_pos_in_range = True
            x_pos_in_range = True

        if y_pos_in_range and x_pos_in_range:
            new_pos_in_range = True

        return new_pos_in_range

    def score_counter(self, gamer):
        if gamer == Gamer.HUMAN:
            self.__score[Gamer.HUMAN] = self.__score[Gamer.HUMAN] + 1
        elif gamer == Gamer.COMPUTER:
            self.__score[Gamer.COMPUTER] = self.__score[Gamer.COMPUTER] + 1

    def get_score(self):
        return self.__score

    def reset_score_counter(self):
        self.__score = [0, 0]
