from machine import Pin, PWM, I2C
from i2c_lcd import I2cLcd
import config

# rgb
led_rojo = Pin(config.LED_ROJO_PIN, Pin.OUT)
led_verde = Pin(config.LED_VERDE_PIN, Pin.OUT)
led_azul = Pin(config.LED_AZUL_PIN, Pin.OUT)

buzzer = PWM(Pin(config.BUZZER_PIN))
buzzer.freq(2000)

i2c = I2C(0, sda=Pin(config.LCD_SDA), scl=Pin(config.LCD_SCL), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)


def establecer_color(rojo, verde, azul):
    led_rojo.value(rojo)
    led_verde.value(verde)
    led_azul.value(azul)

# Buzzer
def buzzer_encender():
    buzzer.duty_u16(32768)


def buzzer_apagar():
    buzzer.duty_u16(0)

# CLD
def lcd_mostrar(linea1, linea2=""):
    lcd.clear()
    lcd.putstr(linea1)
    lcd.move_to(0, 1)
    lcd.putstr(linea2)


def actualizar_indicadores(estado):
    if estado == "DESARMADO":
        establecer_color(0, 0, 1)  # azul
        buzzer_apagar()
    elif estado == "ARMADO":
        establecer_color(0, 1, 0)  # verde
        buzzer_apagar()
    elif estado == "ALARMA":
        establecer_color(1, 0, 0)  # rojo
        buzzer_encender()


def iniciar():
    actualizar_indicadores("DESARMADO")
    lcd_mostrar("Sistema Seg.", "Iniciando...")
