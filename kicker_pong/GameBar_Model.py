class GameBar:

    def __init__(self, position, speed, time_delta):
        self._position = position
        self._next_position = -1
        self._speed = speed
        self._time = time_delta

    def get_position(self):
        return self._position

    def set_position(self, pos):
        self._position = pos

    def get_next_position(self):
        return self._next_position

    def set_next_position(self, next_pos):
        self._next_position = next_pos

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

    def get_time(self):
        return self._time
