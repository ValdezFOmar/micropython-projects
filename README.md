# MicroPython Projects

Proyectos de micropython para la clase **Sistemas Programables**, impartida por el profesor
[**René Solis**](https://github.com/IoTeacher).

## Material utilizado

- Raspberry Pi Pico W
- Micropython v1.20
- Display OLED SSD1306
- Protoboard
- Cables, LEDs y equipo de electronica en general

## Notas y Tips

### Entorno Virtual y Paquetes

Crear un entorno virtual de python:

```sh
python -m venv .venv
source .venv/bin/activate
```

Instalar los paquetes de [`requirements.txt`](./requirements.txt):

```sh
pip install -r requirements.txt
```

Estos paquetes permiten una mejor experiencia para programar en micorpython:

1.  `rshell`: Permite realizar una comunicación serial con la REPL de la Pico W, así como terner acceso
    a distintos comando muy utiles.
2.  [`stubs`](https://github.com/Josverl/micropython-stubs) para micropython: Estos son archivos que representan la interfaz de los modulos, funciones,
    metodos, clases, etc. implementados en micropython. Ofrecen documentación y una mejor integración con
    analizadores estaticos y linters.
3.  [`picozero`](https://picozero.readthedocs.io/en/latest/): Una libreria para facilitar la comunicación con componentes lectronicos.

### Extra

[`pycon`](./pycon) es un script en bash para automatizar acciones repetitivas utilizando `rshell`. Para activarlo:

```sh
source pycon
```

Para desactivarlo:

```sh
desc
```
