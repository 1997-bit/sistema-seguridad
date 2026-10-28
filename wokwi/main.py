# Loop principal: boton, intrusion, LCD y telemetria

from time import sleep_ms
import sensores
import actuadores
import alarma


def procesar_comando(accion, origen):
    resultado = alarma.ejecutar_comando(accion)
    print("[CMD]", {"action": accion, "source": origen, "result": resultado})
    return resultado


def enviar_telemetria():
    # TODO: publicar por MQTT
    print("[TELEMETRIA]", {
        "motion": int(sensores.hay_movimiento()),
        "distance": sensores.medir_distancia(),
        "state": alarma.estado,
    })


def main():
    actuadores.iniciar()

    boton_antes = False
    estado_antes = None
    vueltas = 0

    while True:
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
            print("[EVENTO]", {"type": "intrusion", "sensor": sensor})

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
