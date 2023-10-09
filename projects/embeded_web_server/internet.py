import socket
from time import sleep

import network
from env import getenv
from machine import Pin

PICO_LED = Pin("LED", Pin.OUT)


def connect_wlan(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)  # IP

    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)

    return wlan.ifconfig()[0]  # IP


def open_socket(ip, port=80):
    address = (ip, port)
    connection = socket.socket()

    # Needed for reusing a bound address (OSError: [Errno 98] EADDRINUSE)
    # See: https://github.com/micropython/micropython/issues/3739#issuecomment-386191815
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    connection.bind(address)
    connection.listen(1)
    return connection


def web_page(state):
    html = f"""
    <!DOCTYPE html>
    <html>

    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Pico W Server</title>
    </head>

    <body>
      <form action="./lighton">
        <input type="submit" value="Light on" />
      </form>
      <form action="./lightoff">
        <input type="submit" value="Light off" />
      </form>
      <p>LED is {state}</p>
    </body>

    </html>
    """
    return str(html)


def serve(connection: socket.socket):
    global PICO_LED

    print("Serving...")

    state = "OFF"
    PICO_LED.off()

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)

        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == "/lighton?":
            PICO_LED.on()
            state = "ON"
        elif request == "/lightoff?":
            PICO_LED.off()
            state = "OFF"

        html = web_page(state)
        client.send(html)

        client.close()


def main():
    ssid = getenv("SSID")
    passwd = getenv("PASSWORD")

    ip = connect_wlan(ssid, passwd)
    print(f"\nIP Address: {ip}")

    connection = open_socket(ip)
    try:
        serve(connection)
    finally:
        connection.close()
        print("Closing connection...")


if __name__ == "__main__":
    main()
