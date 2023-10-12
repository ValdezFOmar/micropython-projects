"""
# Actividad 2.2: Desplegar temperatura en OLED Display con bitArray imagen

- Alumno: Valdez Fuentes Omar Antonio
- Materia: Sistemas Programables
- Profesor: René Solis Reyes


Referencias tomadas para la practica:

1. Como convertir los valores de la pico a celsius:
    https://how2electronics.com/read-temperature-sensor-value-from-raspberry-pi-pico/
2. Datasheet de la Pico W (temperaturas maximas):
    https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf
"""

import temp_images
import utime
from machine import ADC, I2C, Pin
from ssd1306 import SSD1306_I2C

# Display dimensions in pixels
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Maximun operable temperatures in celsius
MAX_TEMPERATURE = 70
MIN_TEMPERATURE = -20

# Constants for converting the values returned by the pico
# to volts and then to celsius
PICO_MAX_VOLTS = 3.3
MAX_16_BIT_INTEGER = 2**16 - 1
CELSIUS_REFERENCE = 27
CELSIUS_REFERENCE_TO_VOLTS = 0.706
VOLTS_BY_CELSIUS = 0.001721


def convert_celsius(sensor: ADC):
    # La lectura de la Pico W se encuentra entre el rango de 0 al valor maximo
    # de un entero de 16 bits y es proporcional al rango 0 a la maxima cantidad
    # de volts suministrada por la pico (3.3v)
    conversion_factor = PICO_MAX_VOLTS / MAX_16_BIT_INTEGER
    volts_reading = sensor.read_u16() * conversion_factor

    # La diferencia en celsius del punto de referencia y la lectura en volts
    celsius_difference = (volts_reading - CELSIUS_REFERENCE_TO_VOLTS) / VOLTS_BY_CELSIUS

    # Se calcula la temperatura restando la diferencia en celcius del punto de referencia
    temperature = CELSIUS_REFERENCE - celsius_difference
    return temperature


def image_to_show(temperature: float):
    # Se utiliza un rango de tolerancia de 20 celsius antes de llegar
    # a las temperaturas maximas operacionales para la Pico W
    tolerance = 20
    if temperature >= (MAX_TEMPERATURE - tolerance):
        return temp_images.HOT
    elif temperature <= (MIN_TEMPERATURE + tolerance):
        return temp_images.COLD
    else:
        return temp_images.NORMAL


def main():
    i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=200000)
    oled = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
    temperature_sensor = ADC(4)

    while True:
        # print("16 bit temperature reading:", temperature_sensor.read_u16())
        temperature = convert_celsius(temperature_sensor)
        oled.fill(0)
        oled.text("Temperature", 0, 0)
        oled.text(f"{temperature:.2f} Celsius", 0, 10)

        image = image_to_show(temperature)
        oled.blit(
            # Displeaga la imagen centrada en el Display
            image.image,
            image.center_width(DISPLAY_WIDTH),
            image.center_height(DISPLAY_HEIGHT) + 10,
        )

        oled.show()
        utime.sleep_ms(100)


if __name__ == "__main__":
    main()
