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
from openai import OpenAIRequest
from picozero import Button

from micropython import const

SSID = getenv("SSID")
PASSWORD = getenv("PASSWORD")
OPEN_AI_API_KEY = getenv("OPEN_AI_API_KEY")
CHATGPT_PROMPT = const(
    """escribe una historia corta de terror con 128 caracteres como maximo"""
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


def display_response(response):
    print(format_text(response, 128 // 8))
    print(response)


def main():
    new_response_button = Button(22)
    chatgpt_api = OpenAIRequest(OPEN_AI_API_KEY)

    connect_wlan(SSID, PASSWORD)
    print("Presiona el boton para generar un historia de terror")

    new_response_button.when_pressed = lambda: display_response(
        chatgpt_api.get_chatgpt_response(CHATGPT_PROMPT)
    )


if __name__ == "__main__":
    main()
