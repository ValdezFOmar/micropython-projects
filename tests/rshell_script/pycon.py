from rshell import pyboard

commands = """
import time
from machine import Pin

Pin('LED', Pin.OUT).on()
time.sleep(5)
Pin('LED', Pin.OUT).off()
"""


def main():
    port = "/dev/ttyACM0"
    pico_w = pyboard.Pyboard(port)

    pico_w.enter_raw_repl()
    pico_w.exec_(commands)
    pico_w.exit_raw_repl()


if __name__ == "__main__":
    main()
