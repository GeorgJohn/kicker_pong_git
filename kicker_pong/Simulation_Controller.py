import pygame
import random
from src.Constant import *
from src import Simulation_View
from src import Ball_Model
from src import Kicker_Model
from src import HumanKeeper_Model
from src import ComputerKeeper_Model
from src.SimpleHumanAI_Controller import SimpleHumanAI
from src.ManualComputerKeeper_Controller import ManualKeeperController

random.seed()

ball_start_pos_x = COURT_WIDTH / 2  # random.randint(20, Const.COURT_WIDTH - 20)
ball_start_pos_y = COURT_HEIGHT / 2  # random.randint(20, Const.COURT_HEIGHT - 20)  # Position wo der Ball startet
ball_start_pos_z = 0
ball_speed = 1 * 1000  # Geschwindigkeit in m/s
ball_angle = random.uniform(math.pi / 4, - math.pi / 4)  # 3/2 * math.pi + 0.1  #
ball_angle_speed = 1.0
time_delta = 1 / 60
acceleration_bar = 2 * 1000  # Beschleunigung in m/s^2
speed = 500  # Stangen maximal Geschwindigkeit in m/s

clock = pygame.time.Clock()
my_view = Simulation_View.View()
my_ball = Ball_Model.Ball(x_pos=ball_start_pos_x, y_pos=ball_start_pos_y, speed=ball_speed,
                          angle=ball_angle, time_delta=time_delta)
my_kicker = Kicker_Model.Kicker(time_delta)
my_human_keeper = HumanKeeper_Model.HumanKeeper(speed, time_delta)
my_human_strategy = SimpleHumanAI()

my_computer_keeper = ComputerKeeper_Model.ComputerKeeper(speed, time_delta)
my_manual_controller = ManualKeeperController()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                my_manual_controller.set_move_up()
            elif event.key == pygame.K_UP:
                my_manual_controller.set_move_down()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                my_manual_controller.reset_move_bar()
        elif event.type == pygame.QUIT:
            running = False

    my_manual_controller.move_bar(my_computer_keeper)

    my_human_strategy.new_strategy_step(my_human_keeper, my_ball)

    my_ball.move(my_kicker, my_computer_keeper, my_human_keeper)
    if my_ball.get_terminal():
        my_ball.kick_off()
        my_ball.set_terminal(False)

    my_view.display_empty_screen()
    my_view.display_court_line()
    my_view.display_info()
    my_view.display_ball(my_ball)
    my_view.display_human_figures(my_human_keeper)
    my_view.display_computer_figures(my_computer_keeper)
    my_view.display_score(my_kicker.get_score())

    clock.tick_busy_loop(60)

    pygame.display.flip()  # Fenster anzeigen

