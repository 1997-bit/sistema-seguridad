# alarm.py
# Sistema de Seguridad IoT
# Maquina de estados de la alarma
# Gloria - Parcial #2 DS8

import config
import actuators
import sensors

DISARMED = "DISARMED"
ARMED = "ARMED"
ALARM = "ALARM"

_state = DISARMED


def get_state():
    return _state


def _set_state(new_state):
    global _state
    _state = new_state
    actuators.update_indicators(_state)


def check_intrusion():
    """Devuelve (sensor, motivo) si hay intrusion, si no None."""
    if sensors.read_motion():
        return ("pir", "motion")
    if sensors.door_open():
        return ("door", "opened")
    dist = sensors.read_distance()
    if dist is not None and dist < config.DISTANCE_ALERT_CM:
        return ("ultrasonic", "proximity")
    return None


def update():
    """Evalua sensores y dispara alarma si esta armada. Devuelve info o None."""
    global _state
    if _state != ARMED:
        return None
    intr = check_intrusion()
    if intr is not None:
        _set_state(ALARM)
        return ("intrusion", intr)
    return None


def arm():
    if _state == DISARMED:
        _set_state(ARMED)
        return "ok"
    return "error"


def disarm():
    _set_state(DISARMED)
    return "ok"


def silence():
    if _state == ALARM:
        _set_state(ARMED)
        return "ok"
    return "error"


def lock():
    actuators.lock()
    return "ok"


def unlock():
    actuators.unlock()
    return "ok"


def handle_command(action):
    """Procesa un comando de texto y devuelve 'ok' o 'error'."""
    action = str(action).strip().lower()
    if action == "arm":
        return arm()
    if action == "disarm":
        return disarm()
    if action == "silence":
        return silence()
    if action == "lock":
        return lock()
    if action == "unlock":
        return unlock()
    return "error"


# Inicializar indicadores en estado desarmado
_set_state(DISARMED)