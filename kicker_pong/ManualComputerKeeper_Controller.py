from kicker_pong.ComputerKeeper_Model import ComputerKeeper
from kicker_pong.Constant import *
import pygame
from pygame.locals import *


class ManualKeeperController:
    def __init__(self):
        self.__move_up_flag = False
        self.__move_down_flag = False

    def move_bar(self, gamer_bar):
        if self.__move_up_flag:
            self.move_down(gamer_bar)
        elif self.__move_down_flag:
            self.move_up(gamer_bar)
        else:
            self.reset_move_bar()

    # keydown handler
    @staticmethod
    def move_down(gamer_bar):
        if gamer_bar.get_position() < MAX_POS_KEEPER:
            new_position = gamer_bar.get_position() + gamer_bar.get_speed() * gamer_bar.get_time()
            if new_position > MAX_POS_KEEPER:
                gamer_bar.set_position(MAX_POS_KEEPER)
            else:
                gamer_bar.set_position(new_position)

    # keyup handler
    @staticmethod
    def move_up(gamer_bar):
        if gamer_bar.get_position() > 0:
            new_position = gamer_bar.get_position() - gamer_bar.get_speed() * gamer_bar.get_time()
            if new_position < 0:
                gamer_bar.set_position(0)
            else:
                gamer_bar.set_position(new_position)

    def reset_move_bar(self):
        self.__move_up_flag = False
        self.__move_down_flag = False

    def set_move_up(self):
        self.__move_up_flag = True
        self.__move_down_flag = False

    def set_move_down(self):
        self.__move_up_flag = False
        self.__move_down_flag = True
