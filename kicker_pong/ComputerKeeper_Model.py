from kicker_pong.GameBar_Model import GameBar
from kicker_pong.Constant import *


class ComputerKeeper(GameBar):
    """Konstanten"""
    NUMBER_OF_FIGURES = 1
    DISTANCE_FIGURES = 0
    # MAX_POS_KEEPER = 242
    POSITION_ON_BAR = FIGURE_HEIGHT / 2
    ABS_X_POSITION = X_POSITION_KEEPER
    X_REFLECTION_PLANE = ABS_X_POSITION + FIGURE_WIDTH / 2 + BALL_RADIUS
    X_OFFSET_REFLECTION_PLANE = FIGURE_WIDTH / 2 + BALL_RADIUS
    Y_OFFSET_REFLECTION_PLANE = FIGURE_HEIGHT / 2 + BALL_RADIUS

    def __init__(self, speed, time_delta):
        super().__init__(MAX_POS_KEEPER / 2, speed, time_delta)

    def check_for_interaction(self, ball):
        if ball.get_x_position() > self.X_REFLECTION_PLANE:
            if ball.get_x_position() - self.X_REFLECTION_PLANE <= ball.get_x_position() - ball.get_new_x_position():
                shoot = self.check_for_shoot(ball)
            else:
                shoot = False
            side_collision = False
        elif self.X_REFLECTION_PLANE - ball.get_x_position() < (ball.get_speed() * self._time
                                                                + 2 * self.X_OFFSET_REFLECTION_PLANE):
            side_collision = self.check_for_side_collision(ball)
            shoot = False
        else:
            side_collision = False
            shoot = False
        return shoot, side_collision

    def check_for_shoot(self, ball):
        intersection = ball.get_y_position() - math.tan(ball.get_angle())\
                       * (ball.get_x_position() - self.X_REFLECTION_PLANE)
        if self._position + self.POSITION_ON_BAR - self.Y_OFFSET_REFLECTION_PLANE < intersection \
                < self._position + self.POSITION_ON_BAR + self.Y_OFFSET_REFLECTION_PLANE:
            self.shoot(ball, intersection)
            shoot = True
        else:
            shoot = False
        return shoot

    def shoot(self, ball, intersection):
        delta_t_collision = (ball.get_x_position() - self.X_REFLECTION_PLANE) / \
                            (math.cos(ball.get_angle()) * ball.get_speed())
        shoot_offset = self._position + self.POSITION_ON_BAR - intersection
        ball.set_new_angle((math.pi / 3) * (- shoot_offset / (FIGURE_HEIGHT / 2 + BALL_RADIUS)))
        ball.set_speed(SHOOT_SPEED)
        ball.set_new_y_position(intersection +
                                math.sin(ball.get_new_angle()) * ball.get_speed() * (self._time - delta_t_collision))
        ball.set_new_x_position(self.X_REFLECTION_PLANE +
                                math.cos(ball.get_new_angle()) *
                                ball.get_speed() * (self._time - delta_t_collision))

    def check_for_side_collision(self, ball):
        if ball.get_y_position() < self._position + self.POSITION_ON_BAR - self.Y_OFFSET_REFLECTION_PLANE \
                and ball.get_angle() > 0:
            if ball.get_new_y_position() > self._position + self.POSITION_ON_BAR - self.Y_OFFSET_REFLECTION_PLANE:
                intersection = ball.get_x_position()\
                               + (self._position + self.POSITION_ON_BAR - self.Y_OFFSET_REFLECTION_PLANE
                                  - ball.get_y_position()) / math.tan(ball.get_angle())
                if self.ABS_X_POSITION - self.X_OFFSET_REFLECTION_PLANE < intersection \
                        < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (self._position + self.POSITION_ON_BAR - self.Y_OFFSET_REFLECTION_PLANE
                                         - ball.get_y_position()) / (math.sin(ball.get_angle()) * ball.get_speed())
                    ball.set_new_angle(- ball.get_angle())
                    ball.set_new_x_position(ball.get_x_position() +
                                            math.cos(ball.get_angle()) * ball.get_speed() * self._time)
                    ball.set_new_y_position(self._position + self.POSITION_ON_BAR - self.Y_OFFSET_REFLECTION_PLANE
                                            + math.sin(ball.get_new_angle())
                                            * ball.get_speed() * (self._time - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False
            else:
                side_collision = False
        elif ball.get_y_position() > self._position + self.POSITION_ON_BAR + self.Y_OFFSET_REFLECTION_PLANE \
                and ball.get_angle() < 0:
            if ball.get_new_y_position() < self._position + self.POSITION_ON_BAR + self.Y_OFFSET_REFLECTION_PLANE:
                intersection = ball.get_x_position() \
                               + (ball.get_y_position() - self._position - self.POSITION_ON_BAR
                                  - self.Y_OFFSET_REFLECTION_PLANE) / math.tan(ball.get_angle())
                if self.ABS_X_POSITION - self.X_OFFSET_REFLECTION_PLANE < intersection \
                        < self.ABS_X_POSITION + self.X_OFFSET_REFLECTION_PLANE:
                    delta_t_collision = (ball.get_y_position() - self._position - self.POSITION_ON_BAR
                                         - self.Y_OFFSET_REFLECTION_PLANE)\
                                        / (math.sin(ball.get_angle()) * ball.get_speed())
                    ball.set_new_angle(- ball.get_angle())
                    ball.set_new_x_position(ball.get_x_position() +
                                            math.cos(ball.get_angle()) * ball.get_speed() * self._time)
                    ball.set_new_y_position(self._position + self.POSITION_ON_BAR + self.Y_OFFSET_REFLECTION_PLANE
                                            + math.sin(ball.get_new_angle())
                                            * ball.get_speed() * (self._time - delta_t_collision))
                    side_collision = True
                else:
                    side_collision = False
            else:
                side_collision = False
        else:
            side_collision = False

        return side_collision
