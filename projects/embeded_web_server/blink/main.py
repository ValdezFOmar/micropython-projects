import sys

import network
from env import getenv
from icons import WIFI_ANIMATION, WIFI_ICON_ERROR, WIFI_ICON_FULL
from internet import Server, connect_wlan, handle_connection
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

from micropython import const


def handle_connection_animation(wlan: network.WLAN, display: SSD1306_I2C) -> str:
    x = WIFI_ANIMATION.get_width_center(display.width)
    y = WIFI_ANIMATION.get_height_center(display.height)
    # WIFI_ANIMATION.start_animation(display, x, y)
    MAX_TRIES = const(15)

    ip = ""
    try:
        ip = handle_connection(wlan, MAX_TRIES)
    except RuntimeError:
        # WIFI_ANIMATION.end_animation()
        display.blit(WIFI_ICON_ERROR.buffer, x, y)
        display.show()
        sys.exit()

    # WIFI_ANIMATION.end_animation()
    font_size = 8
    text_x = (display.width - len(ip) * font_size) // 2
    text_y = display.height - font_size

    display.blit(WIFI_ICON_FULL.buffer, x, y)
    display.text(ip, text_x, text_y)
    display.show()

    return ip


def handle_request(request: str, led: Pin):
    # Removes '/' at the start and '?' at the end
    option = request[1:-1]

    if option == "on":
        led.on()
    elif option == "off":
        led.off()


def main():
    WIDTH = const(128)
    HEIGHT = const(64)
    PASSWORD = getenv("PASSWORD")
    SSID = getenv("SSID")

    pico_led = Pin("LED")
    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

    wlan = connect_wlan(SSID, PASSWORD)
    ip = handle_connection_animation(wlan, display)
    # ip = handle_connection(wlan, 20)

    server = Server(ip)
    server.load_html()
    server.open_socket()

    try:
        server.serve(handle_request, pico_led)
    finally:
        server.close_socket()
        pico_led.off()


if __name__ == "__main__":
    main()
