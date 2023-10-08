import max7219
from machine import SPI, Pin

spi = SPI(0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

num_matrices = 1
display = max7219.Matrix8x8(spi, cs, num_matrices)

display.brightness(10)

face = [
    (1, 1),
    (1, 2),
    (1, 5),
    (1, 6),
    (2, 1),
    (2, 2),
    (2, 5),
    (2, 6),
    (3, 3),
    (3, 4),
    (4, 2),
    (4, 3),
    (4, 4),
    (4, 5),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (6, 2),
    (6, 5),
]

while True:
    for y, x in face:
        display.pixel(x, y, 1)
    display.show()
