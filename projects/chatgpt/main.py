"""
# 2.4 Elabore una solución con Pico W (oled display) + botón y ChatGTP

- Alumno: Valdez Fuentes Omar Antonio
- Materia: Sistemas Programables
- Docente: Rene Solis Reyes

Tema a tratar: Historia corta de terror

## Referencias:
1. [HTTP Status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#successful_responses)
2. [`urequests` library](https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html)
3. [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/making-requests)
"""

import io
from time import sleep

import network
from env import getenv
from machine import I2C, Pin
from openai import OpenAIRequest
from picozero import Button
from ssd1306 import SSD1306_I2C

from micropython import const

WIDTH = const(128)
HEIGHT = const(64)


SSID = getenv("SSID")
PASSWORD = getenv("PASSWORD")
OPEN_AI_API_KEY = getenv("OPEN_AI_API_KEY")
CHATGPT_PROMPT = const(
    """escribe una historia corta de terror con 128 caracteres como maximo sin utilizar acentos"""
)


def connect_wlan(ssid: str, password: str) -> str:
    TRIES = 15
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(TRIES):
        if wlan.isconnected():
            break
        sleep(1)

    if wlan.status() != network.STAT_GOT_IP:
        raise RuntimeError("Timeout reached. Failed to connect.")
    return wlan.ifconfig()[0]


def format_text(text: str, max_horizontal_chars: int) -> str:
    new_text = io.StringIO()
    current_lenght = 0

    for char in text:
        if current_lenght == 0 and char == " ":
            continue

        if current_lenght >= max_horizontal_chars:
            current_lenght = 0
            if char not in ("\n", " "):
                current_lenght += 1
            new_text.write("\n" + char.strip())
            continue

        new_text.write(char)
        current_lenght += 1

    return new_text.getvalue()


def display_response(response: str, display: SSD1306_I2C):
    font_size = 8
    formatted_text = format_text(response, display.width // font_size)

    display.fill(0)
    for i, line in enumerate(formatted_text.splitlines()):
        x = 0
        y = i * font_size
        display.text(line, x, y)
    try:
        display.show()
    except OSError:
        print("Display error")


def make_request(chatgpt_api: OpenAIRequest, display: SSD1306_I2C):
    # if chatgpt_api.waiting_for_request:
    #    return

    display_response("Waiting for response...", display)
    response = chatgpt_api.get_chatgpt_response(CHATGPT_PROMPT)
    display_response(response, display)


def main():
    new_response_button = Button(22)
    chatgpt_api = OpenAIRequest(OPEN_AI_API_KEY)

    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

    connect_wlan(SSID, PASSWORD)
    display_response(
        "Presiona el boton para generar una historia corta de terror.", display
    )
    display.show()

    new_response_button.when_pressed = lambda: make_request(chatgpt_api, display)


if __name__ == "__main__":
    main()
