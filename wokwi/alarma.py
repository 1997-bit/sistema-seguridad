import config
import actuadores
import sensores

DESARMADO = "DESARMADO"
ARMADO = "ARMADO"
ALARMA = "ALARMA"

estado = DESARMADO


def cambiar_estado(nuevo):
    global estado
    print("[ALARMA]", estado, "->", nuevo)
    estado = nuevo
    actuadores.actualizar_indicadores(estado)


def detectar_intrusion():
    if sensores.hay_movimiento():
        return "pir"
    distancia = sensores.medir_distancia()
    if distancia is not None and distancia < config.DISTANCIA_ALERTA_CM:
        return "ultrasonic"
    return None


def revisar():
    if estado != ARMADO:
        return None
    sensor = detectar_intrusion()
    if sensor:
        cambiar_estado(ALARMA)
    return sensor


def ejecutar_comando(accion):
    if accion == "armar" and estado == DESARMADO:
        cambiar_estado(ARMADO)
    elif accion == "desarmar":
        cambiar_estado(DESARMADO)
    elif accion == "silenciar" and estado == ALARMA:
        # Solo apaga buzzer, sigue en ALARMA
        actuadores.buzzer_apagar()
    else:
        return "error"
    return "ok"
