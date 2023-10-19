import fb_images
from ssd1306 import SSD1306_I2C

from micropython import const


class MenuOption:
    def __init__(self, image: fb_images.Image, action) -> None:
        self.image = image
        self.action = action


class MenuOptionsContainer:
    GAP = const(4)

    def __init__(
        self,
        header: fb_images.Image,
        options: list[MenuOption],
        select_icon: fb_images.Image,
        selected: int = 0,
    ) -> None:
        self.header = header
        self.options = options
        self.select_icon = select_icon
        self.selected = selected
        self.is_active = True

    def next_option(self):
        if self.selected == len(self.options) - 1:
            self.selected = 0
            return
        self.selected += 1

    def previous_option(self):
        if self.selected == 0:
            self.selected = len(self.options) - 1
            return
        self.selected -= 1

    def _draw_header(self, display: SSD1306_I2C):
        center = self.header.get_width_center(display.width)
        display.blit(self.header.buffer, center, 0)

    def _draw_options(self, display: SSD1306_I2C):
        X_OFFSET = self.select_icon.width + self.GAP
        Y_OFFSET = self.header.height + self.GAP
        OPTION_SIZE = self.select_icon.height

        for i, option in enumerate(self.options):
            x = X_OFFSET
            y = (i * OPTION_SIZE) + Y_OFFSET
            display.blit(option.image.buffer, x, y)

    def _draw_select(self, display: SSD1306_I2C):
        Y_OFFSET = self.header.height + self.GAP
        y = (self.selected * self.select_icon.height) + Y_OFFSET
        display.blit(self.select_icon.buffer, 0, y)

    def draw_menu(self, display: SSD1306_I2C):
        self._draw_header(display)
        self._draw_options(display)
        self._draw_select(display)
