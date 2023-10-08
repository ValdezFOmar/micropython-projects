import framebuf
from logo import ISC_LOGO
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64


def display_logo(oled, image):
    fb = framebuf.FrameBuffer(image, 45, 45, framebuf.MONO_HLSB)
    oled.blit(fb, (WIDTH - 45) // 2, 12)


def main():
    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    oled.text("Hola Mundo!", 0, 0)
    display_logo(oled, ISC_LOGO)
    oled.show()


if __name__ == "__main__":
    main()
