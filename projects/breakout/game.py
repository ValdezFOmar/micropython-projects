from display import Display
from physics import Vector2D

from micropython import const

MILLI_SECONDS = const(1000)
FRAMES = const(60)
DELTA_TIME = const(1 / FRAMES)


class Box:
    def __init__(self, width: int, height) -> None:
        pass


class Brick:
    pass


class Ball:
    def __init__(
        self,
        initial_position: Vector2D,
        initial_velocity: Vector2D,
        initial_acceleration: Vector2D = Vector2D(0, 0),
    ) -> None:
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration

    def update(self):
        """Updates the state of the object (position, velocity, ...)"""
        self.position += self.velocity
        print(self.position)

    def on_collision(self):
        ...

    def draw(self, display: Display):
        ...


class Platform:
    pass
