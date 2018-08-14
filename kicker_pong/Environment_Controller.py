import pygame
import random
from kicker_pong.Constant import *
from kicker_pong.Simulation_View import View
from kicker_pong.Kicker_Model import Kicker
from kicker_pong.Ball_Model import Ball
from kicker_pong.ComputerKeeper_Model import ComputerKeeper
from kicker_pong.HumanKeeper_Model import HumanKeeper
from kicker_pong.Environment_Model import EnvironmentModel
from kicker_pong.SimpleHumanAI_Controller import SimpleHumanAI

# KEEPER_START_POS = MAX_POS_KEEPER / 2
BALL_START_POS_X = COURT_WIDTH / 2
BALL_START_POS_Y = COURT_HEIGHT / 2
BALL_START_SPEED = 1.0 * 500
BAR_SPEED = 1.0 * 400
TIME_STEP = 1 / 60


class Action(IntEnum):
    NOOP = 0
    UP = 1
    DOWN = 2


class ActionHandler:

    def __init__(self, gamer_bar):
        self.gamer_bar = gamer_bar

    def move_bar(self, action):
        if action == Action.UP:
            self.move_up()
        elif action == Action.DOWN:
            self.move_down()
        elif action == Action.NOOP:
            self.no_move()
        else:
            print("undefined action !!!")

    def move_up(self):
        if self.gamer_bar.get_position() > 0:
            new_position = self.gamer_bar.get_position() - self.gamer_bar.get_speed() * self.gamer_bar.get_time()
            if new_position < 0:
                self.gamer_bar.set_position(0)
            else:
                self.gamer_bar.set_position(new_position)

    def move_down(self):
        if self.gamer_bar.get_position() < MAX_POS_KEEPER:
            new_position = self.gamer_bar.get_position() + self.gamer_bar.get_speed() * self.gamer_bar.get_time()
            if new_position > MAX_POS_KEEPER:
                self.gamer_bar.set_position(MAX_POS_KEEPER)
            else:
                self.gamer_bar.set_position(new_position)

    def no_move(self):
        self.gamer_bar.set_position(self.gamer_bar.get_position())


class EnvironmentController:

    def __init__(self):
        random.seed()
        # angle = math.pi
        angle = random.uniform(- math.pi/12, math.pi/12)
        if angle > 0:
            angle -= math.pi
        else:
            angle += math.pi

        self.env = EnvironmentModel()
        self.kicker = Kicker(TIME_STEP)
        self.ball = Ball(x_pos=BALL_START_POS_X, y_pos=BALL_START_POS_Y, speed=BALL_START_SPEED,
                         angle=angle, time_delta=TIME_STEP)
        self.computer_keeper = ComputerKeeper(BAR_SPEED, TIME_STEP)
        self.human_keeper = HumanKeeper(BAR_SPEED, TIME_STEP)
        self.human_strategy = SimpleHumanAI()
        self.action_handler = ActionHandler(self.computer_keeper)
        self.create_view = False
        self.view = None

    def reset(self):
        self.env.set_done(False)
        self.ball.kick_off()
        if self.kicker.get_score()[0] >= 10 or self.kicker.get_score()[1] >= 10:
            self.kicker.reset_score_counter()
            self.env.set_old_score([0, 0])

        self.computer_keeper.set_position(MAX_POS_KEEPER / 2)
        self.human_keeper.set_position(MAX_POS_KEEPER / 2)
        self.env.update(self.kicker, self.ball, self.computer_keeper, self.human_keeper)
        self.env.update(self.kicker, self.ball, self.computer_keeper, self.human_keeper)
        self.env.set_reward(0)
        return self.env.get_observation()

    def render(self):
        if not self.create_view:
            self.view = View()
            self.create_view = True
        self.view.display_empty_screen()
        self.view.display_court_line()
        self.view.display_info()
        self.view.display_ball(self.ball)
        self.view.display_computer_figures(self.computer_keeper)
        self.view.display_human_figures(self.human_keeper)
        self.view.display_score(self.kicker.get_score())

        pygame.display.flip()

    def step(self, action):

        self.human_strategy.new_strategy_step(self.human_keeper, self.ball)
        for i in range(2):
            self.action_handler.move_bar(action)
            self.ball.move(self.kicker, self.computer_keeper,  self.human_keeper)
            self.env.update(self.kicker, self.ball, self.computer_keeper, self.human_keeper)
            if self.check_for_done():
                break

        self.env.calc_reward(self.ball.get_computer_shoot_flag())
        return [self.env.get_observation(), self.env.get_reward(), self.env.get_done()]

    def check_for_done(self):
        if self.ball.get_terminal():
            self.ball.kick_off()
            self.ball.set_terminal(False)
            self.env.set_done(True)
        else:
            self.env.set_done(False)

        return self.env.get_done()

    @staticmethod
    def get_random_action():
        random.seed()
        return random.randint(0, 2)

    def get_goal_counter(self):
        return self.env.get_goal_counter()

    def set_goal_counter(self, count):
        self.env.set_goal_counter(count)