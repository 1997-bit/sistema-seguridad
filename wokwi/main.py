# main.py
# Sistema de Seguridad IoT
# Bucle principal: sensores + alarma + actuadores + telemetria
# Gloria - Parcial #2 DS8

import time
import sensors
import actuators
import alarm
import config

# Historial de eventos del sistema: tuplas (tipo, sensor, timestamp_ms)
EVENTS = []
# Historial de comandos: tuplas (accion, fuente, resultado, timestamp_ms)
COMMANDS = []


def log_event(event_type, sensor):
    EVENTS.append((event_type, sensor, time.ticks_ms()))
    print("EVENT", {"type": event_type, "sensor": sensor})


def log_command(action, source, result):
    COMMANDS.append((action, source, result, time.ticks_ms()))
    print("CMD", {"action": action, "source": source, "result": result})


def process_command(action, source="local"):
    result = alarm.handle_command(action)
    log_command(action, source, result)
    return result


def read_sensors():
    return {
        "motion": sensors.read_motion(),
        "distance": sensors.read_distance(),
        "door": sensors.door_open(),
        "button": sensors.button_pressed(),
    }


def main():
    actuators.init_actuators()
    alarm.disarm()
    actuators.lcd_show("Sistema Seg.", "Desarmado")
    time.sleep_ms(500)

    last_button = False

    while True:
        data = read_sensors()

        # Boton fisico: alterna armado/desarmado
        if data["button"] and not last_button:
            if alarm.get_state() == alarm.DISARMED:
                process_command("arm", "button")
            else:
                process_command("disarm", "button")
            time.sleep_ms(200)
        last_button = data["button"]

        # Evaluar intrusion
        intr = alarm.update()
        if intr is not None:
            sensor = intr[1][0] if isinstance(intr[1], tuple) else intr[1]
            log_event("intrusion", sensor)

        # Actualizar indicadores y LCD
        state = alarm.get_state()
        actuators.update_indicators(state)
        dist = data["distance"]
        dist_str = ("%.1f" % dist) if dist is not None else "--"
        actuators.lcd_show(state, "D:" + dist_str + "cm")

        # Telemetria
        print({
            "motion": 1 if data["motion"] else 0,
            "distance": dist,
            "door": 1 if data["door"] else 0,
            "state": state,
        })

        time.sleep_ms(1000)


if __name__ == "__main__":
    main()