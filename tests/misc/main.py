from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)

try:
    print('inicio')
    for _ in range(10):
        print('Turning built-in LED on.')
        led.on()
        sleep(0.5)
        print('Turning built-in LED off.')
        led.off()
        sleep(0.5)
except KeyboardInterrupt as e:
    led.off()
    raise e

