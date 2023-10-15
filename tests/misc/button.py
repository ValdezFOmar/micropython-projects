import time

from machine import Pin

interrupt_flag = False
debounce_time = 0
TIME_INTERVAL_MS = 100


def callback(pin: Pin):
    global interrupt_flag, debounce_time
    if (time.ticks_ms() - debounce_time) > TIME_INTERVAL_MS:
        print(pin.value())
        interrupt_flag = 1
        debounce_time = time.ticks_ms()


def main():
    global interrupt_flag
    button = Pin(14, Pin.IN, Pin.PULL_UP)
    pico_led = Pin("LED", Pin.OUT)

    button.irq(handler=callback, trigger=Pin.IRQ_FALLING)

    while True:
        if interrupt_flag:
            interrupt_flag = False
            pico_led.toggle()


if __name__ == "__main__":
    main()
