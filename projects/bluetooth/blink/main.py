import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from machine import Pin

pico_led = Pin("LED", Pin.OUT)


def on_rx(data: bytes):
    parsed_data = data.decode().strip()
    print("Data received:", parsed_data)

    if parsed_data == "on":
        pico_led.on()
    elif parsed_data == "off":
        pico_led.off()
    else:
        print("Invalid instruction.")


def main():
    ble = bluetooth.BLE()
    sp = BLESimplePeripheral(ble)

    while True:
        if sp.is_connected():
            sp.on_write(on_rx)


if __name__ == "__main__":
    main()
