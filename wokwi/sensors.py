# sensors.py

from machine import Pin, time_pulse_us
from time import sleep_ms
import config

# Inicialización de sensores

_pir = Pin(config.PIR_PIN, Pin.IN)

_trig = Pin(config.TRIG_PIN, Pin.OUT)
_echo = Pin(config.ECHO_PIN, Pin.IN)

_door = Pin(config.DOOR_PIN, Pin.IN, Pin.PULL_UP)

_button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)




def read_motion():
    """
    Retorna True cuando el PIR detecta movimiento.
    """
    return _pir.value() == 1


def read_distance():
    """
    Retorna la distancia en centímetros.
    Si no hay lectura devuelve None.
    """

    _trig.value(0)
    sleep_ms(2)

    _trig.value(1)
    sleep_ms(1)
    _trig.value(0)

    try:
        duration = time_pulse_us(_echo, 1, 30000)

        if duration < 0:
            return None

        distance = (duration * 0.0343) / 2

        return distance

    except Exception:
        return None


def door_open():
    """
    True cuando la puerta está abierta.
    """

    return _door.value() == 1


def button_pressed():
    """
    True mientras el botón está presionado.
    """

    return _button.value() == 0



if __name__ == "__main__":

    while True:

        print({
            "motion": read_motion(),
            "distance": read_distance(),
            "door": door_open(),
            "button": button_pressed()
        })

        sleep_ms(500)