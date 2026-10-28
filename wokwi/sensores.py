from machine import Pin, time_pulse_us
from time import sleep_us
import config

pir = Pin(config.PIR_PIN, Pin.IN)
trig = Pin(config.TRIG_PIN, Pin.OUT)
echo = Pin(config.ECHO_PIN, Pin.IN)
boton = Pin(config.BOTON_PIN, Pin.IN, Pin.PULL_UP)  # 0 presionado


def hay_movimiento():
    return pir.value() == 1


def medir_distancia():
    """cm o None"""
    # Pulso TRIG 10 us
    trig.value(0)
    sleep_us(2)
    trig.value(1)
    sleep_us(10)
    trig.value(0)

    # ECHO alto = ida y vuelta, timeout 30 ms
    duracion = time_pulse_us(echo, 1, 30000)
    if duracion < 0:
        return None
    return duracion * 0.0343 / 2  # sonido 0.0343 cm/us, /2 ida y vuelta


def boton_presionado():
    return boton.value() == 0
