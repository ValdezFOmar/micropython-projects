from picozero import RGBLED


def main():
    led = RGBLED(1, 2, 3)
    try:
        while True:
            led.blink()
    finally:
        led.off()


if __name__ == "__main__":
    main()
