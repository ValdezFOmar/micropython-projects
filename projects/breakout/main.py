# from picozero import Button, pico_led
import io

from display import SSD1306_HEIGHT, SSD1306_WIDTH, DisplaySSD1306
from game import DELTA_TIME, MILLI_SECONDS, Ball
from machine import Timer
from physics import Vector2D

WIDTH = SSD1306_WIDTH
HEIGHT = SSD1306_HEIGHT


ball = Ball(
    initial_position=Vector2D(WIDTH // 2, HEIGHT // 2),
    initial_velocity=Vector2D(2, 2),
)

buffer = io.StringIO()

max_number_loops = 60
current_number_loops = 0


def loop(timer: Timer):
    global current_number_loops

    if not (current_number_loops < max_number_loops):
        with open("positions.txt", "w", encoding="utf-8") as f:
            f.write(buffer.getvalue())
        timer.deinit()
        return

    current_number_loops += 1
    ball.update()
    print(ball.position, file=buffer)


def main():
    # button = Button(14)
    # button.when_pressed = pico_led.toggle

    t = Timer()
    t.init(mode=Timer.PERIODIC, period=int(DELTA_TIME * MILLI_SECONDS), callback=loop)


if __name__ == "__main__":
    main()
