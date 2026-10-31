# Nube: Adafruit IO por MQTT

from umqttsimple import MQTTClient
import secretos

FEEDS = secretos.AIO_USUARIO + "/feeds/"


def conectar(recepcion_comandos):
    print("Conectando a Adafruit IO")
    cliente = MQTTClient("ds8_seguridad_aio", "io.adafruit.com", user=secretos.AIO_USUARIO, password=secretos.AIO_KEY, keepalive=60)
    cliente.set_callback(recepcion_comandos)
    cliente.connect()
    cliente.subscribe(FEEDS + "comandos")
    print("Adafruit conectado")
    return cliente


def publicar(cliente, datos):
    for feed in datos:
        cliente.publish(FEEDS + feed, str(datos[feed]))
