import os

import fb_images
from machine import I2C, Pin
from option_menu import MenuOption, MenuOptionsContainer
from picozero import Button
from ssd1306 import SSD1306_I2C

from micropython import const

WIDTH = const(128)
HEIGHT = const(64)


def up_action(menu: MenuOptionsContainer, display: SSD1306_I2C):
    if not menu.is_active:
        return
    display.fill(0)
    menu.previous_option()
    menu.draw_menu(display)
    display.show()


def down_action(menu: MenuOptionsContainer, display: SSD1306_I2C):
    if not menu.is_active:
        return
    display.fill(0)
    menu.next_option()
    menu.draw_menu(display)
    display.show()


def select_action(menu: MenuOptionsContainer, display: SSD1306_I2C):
    display.fill(0)
    if menu.is_active:
        menu.options[menu.selected].action()
    else:
        menu.draw_menu(display)
    menu.is_active = not menu.is_active
    display.show()


def list_files(display: SSD1306_I2C):
    font_size = const(10)
    for i, file in enumerate(os.listdir("/")):
        display.text(file, 0, i * font_size)


def main():
    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    up_button = Button(27)
    down_button = Button(26)
    select_button = Button(22)

    options = [
        MenuOption(image, func)
        for image, func in (
            (fb_images.FILES_OPTION, lambda: list_files(display)),
            (
                fb_images.DIAGRAM_OPTION,
                lambda: display.blit(fb_images.PICO_DIAGRAM.buffer, 0, 0),
            ),
            (
                fb_images.PICO_LED_OPTION,
                lambda: display.blit(fb_images.PICO_LED_IMAGE.buffer, 0, 0),
            ),
        )
    ]
    menu = MenuOptionsContainer(fb_images.MENU_HEADER, options, fb_images.SELECTION)

    up_button.when_pressed = lambda: up_action(menu, display)
    down_button.when_pressed = lambda: down_action(menu, display)
    select_button.when_pressed = lambda: select_action(menu, display)

    menu.draw_menu(display)
    display.show()


if __name__ == "__main__":
    main()
