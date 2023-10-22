from time import sleep

import icons
from env import getenv
from internet import Server
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

from micropython import const


def main_server():
    server = Server()
    server.connect_wlan(getenv("SSID"), getenv("PASSWORD"))
    server.load_html()
    server.open_socket()

    try:
        server.serve()
    finally:
        server.close_socket()


def wifi_animation(display: SSD1306_I2C):
    icons_sequence = (
        icons.WIFI_ICON_LOW,
        icons.WIFI_ICON_MEDIUM,
        icons.WIFI_ICON_FULL,
    )
    for i, wifi_icon in enumerate(icons_sequence, 1):
        x = wifi_icon.get_width_center(display.width)
        y = wifi_icon.get_height_center(display.height)
        display.blit(wifi_icon.buffer, x, y)
        display.text(f"Conectando{'.' * i}", 0, display.height - 8)
        display.show()
        sleep(0.5)


def main():
    WIDTH = const(128)
    HEIGHT = const(64)

    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

    while True:
        wifi_animation(display)


if __name__ == "__main__":
    main()
