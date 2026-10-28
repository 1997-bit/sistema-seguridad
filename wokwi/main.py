# Loop principal: boton, intrusion, LCD, telemetria y MQTT

from time import sleep_ms
import sensores
import actuadores
import alarma
import mqtt_client

cliente = None


def procesar_comando(accion, origen):
    resultado = alarma.ejecutar_comando(accion)
    print("[CMD]", {"action": accion, "source": origen, "result": resultado})
    return resultado


def recepcion_comandos(topic, msg):
    procesar_comando(msg.decode(), "mqtt")


def enviar_telemetria():
    datos = {
        "motion": int(sensores.hay_movimiento()),
        "distance": sensores.medir_distancia(),
        "state": alarma.estado,
    }
    print("[TELEMETRIA]", datos)
    mqtt_client.publicar(cliente, mqtt_client.TOPIC_PUB_TELEMETRIA, datos)


def main():
    global cliente
    actuadores.iniciar()
    mqtt_client.conectar_wifi()
    cliente = mqtt_client.conectar_broker(recepcion_comandos)

    boton_antes = False
    estado_antes = None
    vueltas = 0

    while True:
        # Comandos que llegan por MQTT
        cliente.check_msg()

        # Boton: solo al presionar
        boton = sensores.boton_presionado()
        if boton and not boton_antes:
            if alarma.estado == alarma.DESARMADO:
                procesar_comando("armar", "boton")
            else:
                procesar_comando("desarmar", "boton")
        boton_antes = boton

        # Intrusion
        sensor = alarma.revisar()
        if sensor:
            datos = {"type": "intrusion", "sensor": sensor}
            print("[EVENTO]", datos)
            mqtt_client.publicar(cliente, mqtt_client.TOPIC_PUB_EVENTOS, datos)

        # LCD solo si cambia estado, evita parpadeo
        if alarma.estado != estado_antes:
            actuadores.lcd_mostrar("Alarma:", alarma.estado)
            estado_antes = alarma.estado

        # Telemetria cada 10 vueltas = 1 s
        vueltas += 1
        if vueltas == 10:
            enviar_telemetria()
            vueltas = 0

        sleep_ms(100)


main()
