from env import getenv
from internet import Server
from picozero import RGBLED


def turn_led_on(request: str, rgb_led: RGBLED):
    # Removes '/' at the start and '?' at the end
    option = request[1:-1]

    if option == "red":
        rgb_led.color = 255, 0, 0
    elif option == "green":
        rgb_led.color = 0, 255, 0
    elif option == "blue":
        rgb_led.color = 0, 0, 255
    elif option == "off":
        rgb_led.off()


def main():
    rgb_led = RGBLED(
        red=2,
        green=3,
        blue=4,
        active_high=False,
    )

    server = Server()
    server.connect_wlan(getenv("SSID"), getenv("PASSWORD"))
    server.load_html()
    server.open_socket()

    try:
        server.serve(turn_led_on, rgb_led)
    finally:
        server.close_socket()
        rgb_led.off()


if __name__ == "__main__":
    main()
