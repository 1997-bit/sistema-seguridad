# Escucha HiveMQ y guarda en MariaDB

import json
import paho.mqtt.client as mqtt
import database


def al_recibir(cliente, userdata, msg):
    datos = json.loads(msg.payload)
    print(msg.topic, datos)
    if msg.topic.endswith("telemetry"):
        database.guardar_lectura(datos)
    elif msg.topic.endswith("events"):
        database.guardar_evento(datos)
    elif msg.topic.endswith("ack"):
        database.guardar_comando(datos)


cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "ds8_seguridad_logger")
cliente.on_message = al_recibir
cliente.connect("broker.hivemq.com", 1883)
cliente.subscribe("ds8/security/pico1/telemetry")
cliente.subscribe("ds8/security/pico1/events")
cliente.subscribe("ds8/security/pico1/ack")
print("Escuchando HiveMQ")
cliente.loop_forever()
