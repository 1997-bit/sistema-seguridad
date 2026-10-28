# Contrato

## Pines

Los define Arles en `wokwi/config.py`.

## Sensores (`wokwi/sensores.py`)

```python
hay_movimiento() -> bool
medir_distancia() -> float | None
boton_presionado() -> bool
```

## Alarma

Estados: `DESARMADO` (azul), `ARMADO` (verde), `ALARMA` (rojo + buzzer). Leer con `alarma.estado`

Comandos: `alarma.ejecutar_comando(accion)` → `"ok"` / `"error"`

| Comando | Qué hace |
|---|---|
| `armar` | DESARMADO → ARMADO |
| `desarmar` | cualquier estado → DESARMADO |
| `silenciar` | apaga el buzzer, sigue en ALARMA |

## MQTT

Broker: `broker.hivemq.com:1883`
Base: `ds8/security/pico1`

| Tópico | Payload |
|---|---|
| `/telemetry` | `{"movimiento":1,"distancia":35.2,"estado":"ARMADO"}` |
| `/events` | `{"tipo":"intrusion","sensor":"pir"}` |
| `/commands` | `armar` |
| `/ack` | `{"accion":"armar","origen":"mqtt","resultado":"ok"}` |

## Base de datos (SQLite)

| Tabla | Columnas |
|---|---|
| `readings` | id, motion, distance, state, timestamp |
| `events` | id, type, sensor, timestamp |
| `commands` | id, action, source, result, timestamp |

## ThingSpeak

| Campo | Dato |
|---|---|
| field1 | motion |
| field2 | distance |
| field3 | state (0, 1, 2) |

Comandos desde la nube: TalkBack.
