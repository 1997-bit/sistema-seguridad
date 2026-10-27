# actuators.py
# Sistema de Seguridad IoT
# Control de actuadores: LEDs, buzzer, servo, LCD I2C
# Gloria - Parcial #2 DS8

from machine import Pin, PWM, I2C
import time
import config

# ----------------------
# LEDs
# ----------------------

_led_red = Pin(config.LED_RED_PIN, Pin.OUT)
_led_green = Pin(config.LED_GREEN_PIN, Pin.OUT)


def led_red(on):
    _led_red.value(1 if on else 0)


def led_green(on):
    _led_green.value(1 if on else 0)


# ----------------------
# Buzzer (PWM)
# ----------------------

_buzzer = PWM(Pin(config.BUZZER_PIN))


def buzzer_on(freq=2000):
    _buzzer.freq(freq)
    _buzzer.duty_u16(32768)


def buzzer_off():
    _buzzer.duty_u16(0)


# ----------------------
# Servo (PWM, 50 Hz)
# ----------------------

_servo = PWM(Pin(config.SERVO_PIN))
_servo.freq(50)

_SERVO_MIN_DUTY = 1638   # ~0.5 ms
_SERVO_MAX_DUTY = 8192   # ~2.5 ms


def servo_angle(deg):
    """Mueve el servo a un angulo entre 0 y 180 grados."""
    if deg < 0:
        deg = 0
    if deg > 180:
        deg = 180
    duty = int(_SERVO_MIN_DUTY + (_SERVO_MAX_DUTY - _SERVO_MIN_DUTY) * deg / 180)
    _servo.duty_u16(duty)


def lock():
    """Cierra la cerradura (servo a 0 grados)."""
    servo_angle(0)


def unlock():
    """Abre la cerradura (servo a 90 grados)."""
    servo_angle(90)


# ----------------------
# LCD I2C (HD44780 via PCF8574)
# ----------------------

_LCD_ADDR = 0x27
_RS = 0x01
_RW = 0x02
_EN = 0x04
_BACKLIGHT = 0x08

_i2c = I2C(0, sda=Pin(config.LCD_SDA_PIN), scl=Pin(config.LCD_SCL_PIN), freq=400000)


def _lcd_write_nibble(nibble, rs=0):
    data = (nibble & 0x0F) << 4
    if rs:
        data |= _RS
    data |= _BACKLIGHT
    try:
        _i2c.writeto(_LCD_ADDR, bytes([data | _EN]))
        time.sleep_us(1)
        _i2c.writeto(_LCD_ADDR, bytes([data & ~_EN]))
        time.sleep_us(50)
    except Exception:
        pass


def _lcd_write_byte(value, rs=0):
    _lcd_write_nibble(value >> 4, rs)
    _lcd_write_nibble(value & 0x0F, rs)


def lcd_init():
    time.sleep_ms(50)
    _lcd_write_nibble(0x03, 0)
    time.sleep_ms(5)
    _lcd_write_nibble(0x03, 0)
    time.sleep_ms(1)
    _lcd_write_nibble(0x03, 0)
    time.sleep_ms(1)
    _lcd_write_nibble(0x02, 0)
    time.sleep_ms(1)
    _lcd_write_byte(0x28)   # 4 bits, 2 lineas, 5x8
    _lcd_write_byte(0x0C)   # display on, cursor off
    _lcd_write_byte(0x06)   # entry mode
    lcd_clear()


def lcd_clear():
    _lcd_write_byte(0x01)
    time.sleep_ms(2)


def lcd_set_cursor(row, col):
    addr = 0x80 + (0x40 if row else 0) + col
    _lcd_write_byte(addr)


def lcd_print(text):
    for ch in str(text):
        _lcd_write_byte(ord(ch), 1)


def lcd_show(line1="", line2=""):
    lcd_clear()
    lcd_set_cursor(0, 0)
    lcd_print(str(line1)[:16])
    lcd_set_cursor(1, 0)
    lcd_print(str(line2)[:16])


# ----------------------
# Indicadores por estado
# ----------------------

def update_indicators(state):
    """Ajusta LEDs y buzzer segun el estado de la alarma."""
    if state == "DISARMED":
        led_red(False)
        led_green(False)
        buzzer_off()
    elif state == "ARMED":
        led_red(False)
        led_green(True)
        buzzer_off()
    elif state == "ALARM":
        led_red(True)
        led_green(False)
        buzzer_on()


def init_actuators():
    led_red(False)
    led_green(False)
    buzzer_off()
    unlock()
    lcd_init()
    lcd_show("Sistema Seg.", "Inicializando")
    time.sleep_ms(500)
