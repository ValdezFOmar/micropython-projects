from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

from micropython import const

SSD1306_WIDTH = const(128)
SSD1306_HEIGHT = const(64)


class Display:
    """Display Interface."""

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def width_center(self):
        return self._width // 2

    @property
    def height_center(self):
        return self._height // 2

    def draw_reactangle(self):
        raise NotImplementedError


class DisplaySSD1306(Display):
    """Display interface for the SSD1306 OLED display."""

    def __init__(
        self,
        sck: int,
        sda: int,
        width: int = SSD1306_WIDTH,
        height: int = SSD1306_HEIGHT,
        freq: int = 200000,
    ) -> None:
        super().__init__(width, height)
        i2c = I2C(0, scl=Pin(sck), sda=Pin(sda), freq=freq)
        self._display = SSD1306_I2C(width, height, i2c)


class AdvancedDisplay(Display):
    pass
