# Wi-Fi y MQTT del Lab 7

import network
import time
from umqttsimple import MQTTClient

SSID = 'Wokwi-GUEST'
PASSWORD = ''

MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = "ds8_seguridad_pico1"

TOPIC_PUB_EVENTOS = b"ds8/security/pico1/events"
TOPIC_PUB_TELEMETRIA = b"ds8/security/pico1/telemetry"
TOPIC_SUB_COMANDOS = b"ds8/security/pico1/commands"


def conectar_wifi():
    print("Conectando a Wi-Fi...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        time.sleep(0.5)
    print("Wi-Fi conectado")


def conectar_broker(recepcion_comandos):
    print("Conectando a", MQTT_BROKER)
    cliente = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    cliente.set_callback(recepcion_comandos)
    cliente.connect()
    cliente.subscribe(TOPIC_SUB_COMANDOS)
    print("MQTT conectado")
    return cliente
