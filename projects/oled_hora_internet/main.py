import time

import framebuf
import time_images
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64


def display_text(oled):
    oled.text("Horario de", 5, 0)
    oled.text("America/Tijuana", 5, 10)


def time_format(hour, minutes):
    f_hour = hour % 12 if hour != 12 else hour
    f_hour = ("0" + str(f_hour)) if f_hour < 10 else f_hour
    f_minutes = ("0" + str(minutes)) if minutes < 10 else minutes
    meridiem = "AM" if hour < 12 else "PM"
    return f"{f_hour}:{f_minutes} {meridiem}"


def match_image_time(hour):
    if 6 <= hour < 12:
        image = time_images.MORNING
    elif 12 <= hour < 20:
        image = time_images.EVENING
    elif (20 <= hour <= 24) or (0 <= hour < 6):
        image = time_images.NIGHT
    else:
        raise ValueError("Hour off limits")
    return framebuf.FrameBuffer(image, 30, 30, framebuf.MONO_HLSB)


def display_time(oled, DEBUG=False):
    last_hour = -1
    last_image = bytearray()
    x_center = (WIDTH - 30) // 2
    # oled.fillrect(x, y, width, height, color)
    text_cover = 5, 20, oled.width - 5, 8, 0

    while True:
        localtime = time.localtime()
        hour, minutes = localtime[3:5]
        oled.fill_rect(*text_cover)
        oled.text(time_format(hour, minutes), 5, 20)

        if hour != last_hour:
            image = match_image_time(hour)
            last_hour = hour
            if image != last_image:
                oled.blit(image, x_center, 30)
                last_image = image

        oled.show()
        if DEBUG:
            print("Local Time:", localtime)
        time.sleep(1)


def main():
    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

    display_text(oled)
    display_time(oled)


if __name__ == "__main__":
    main()
