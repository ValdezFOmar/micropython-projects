"""Testing an common Anode RGB LED"""

from time import sleep

from picozero import RGBLED


def main():
    led = RGBLED(red=2, blue=3, green=4, active_high=False)
    try:
        while True:
            led.color = 255, 0, 0
            sleep(1)
            led.color = 0, 0, 255
            sleep(1)
    finally:
        led.off()


if __name__ == "__main__":
    main()
