import math
from kicker_pong.HumanKeeper_Model import HumanKeeper
from kicker_pong.Constant import *


class SimpleHumanAI:
    def new_strategy_step(self, gamer_bar, ball):
        if - math.pi / 2 < ball.get_angle() < math.pi / 2:
            self._new_desired_pos(gamer_bar, ball.get_y_position() - HumanKeeper.POSITION_ON_BAR)
        else:
            self._new_desired_pos(gamer_bar, MAX_POS_KEEPER/2)

    def _new_desired_pos(self, gamer_bar, desired_pos):
        if 0 <= desired_pos <= MAX_POS_KEEPER:
            gamer_bar.set_next_position(desired_pos)
        elif desired_pos > MAX_POS_KEEPER:
            gamer_bar.set_next_position(MAX_POS_KEEPER)
        elif desired_pos < 0:
            gamer_bar.set_next_position(0)
        self._pos_next_time_step(gamer_bar)

    @staticmethod
    def _pos_next_time_step(gamer_bar):
        if gamer_bar.get_next_position() > gamer_bar.get_position() + 5:
            new_position = gamer_bar.get_position() + gamer_bar.get_speed() * gamer_bar.get_time()
        elif gamer_bar.get_next_position() < gamer_bar.get_position() - 5:
            new_position = gamer_bar.get_position() - gamer_bar.get_speed() * gamer_bar.get_time()
        else:
            new_position = gamer_bar.get_next_position()

        if new_position > MAX_POS_KEEPER:
            gamer_bar.set_position(MAX_POS_KEEPER)
        elif new_position < 0:
            gamer_bar.set_position(0)
        else:
            gamer_bar.set_position(new_position)
