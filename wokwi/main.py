# Loop principal: boton, intrusion, LCD, telemetria, MQTT y Adafruit

from time import sleep_ms
import sensores
import actuadores
import alarma
import mqtt_client
import adafruit

cliente = None
cliente_aio = None


def procesar_comando(accion, origen):
    resultado = alarma.ejecutar_comando(accion)
    datos = {"accion": accion, "origen": origen, "resultado": resultado}
    print("[CMD]", datos)
    mqtt_client.publicar(cliente, mqtt_client.TOPIC_PUB_ACK, datos)
    return resultado


def recepcion_comandos(topic, msg):
    procesar_comando(msg.decode(), "mqtt")


def recepcion_adafruit(topic, msg):
    procesar_comando(msg.decode(), "adafruit")


def enviar_telemetria():
    datos = {
        "movimiento": int(sensores.hay_movimiento()),
        "distancia": sensores.medir_distancia(),
        "estado": alarma.estado,
    }
    print("[TELEMETRIA]", datos)
    mqtt_client.publicar(cliente, mqtt_client.TOPIC_PUB_TELEMETRIA, datos)
    return datos


def main():
    global cliente, cliente_aio
    actuadores.iniciar()
    mqtt_client.conectar_wifi()
    cliente = mqtt_client.conectar_broker(recepcion_comandos)
    cliente_aio = adafruit.conectar(recepcion_adafruit)

    boton_antes = False
    estado_antes = None
    vueltas = 0

    while True:
        # Comandos de HiveMQ y Adafruit
        cliente.check_msg()
        cliente_aio.check_msg()

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
            datos = {"tipo": "intrusion", "sensor": sensor}
            print("[EVENTO]", datos)
            mqtt_client.publicar(cliente, mqtt_client.TOPIC_PUB_EVENTOS, datos)

        # LCD solo si cambia estado, evita parpadeo
        if alarma.estado != estado_antes:
            actuadores.lcd_mostrar("Alarma:", alarma.estado)
            estado_antes = alarma.estado

        # Telemetria cada 1 s, Adafruit cada 10 s (limite 30 datos/min)
        vueltas += 1
        if vueltas % 10 == 0:
            datos = enviar_telemetria()
        if vueltas == 100:
            adafruit.publicar(cliente_aio, datos)
            vueltas = 0

        sleep_ms(100)


# Si se cae la red, reconecta todo
while True:
    try:
        main()
    except OSError as error:
        print("Conexion perdida:", error)
        sleep_ms(5000)
