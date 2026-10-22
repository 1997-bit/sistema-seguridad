# Contrato

## Pines

Los define Arles en `wokwi/config.py`.

## Sensores

```python
read_motion()    -> bool
read_distance()  -> float | None
door_open()      -> bool
button_pressed() -> bool
```

## Alarma

Estados: `DISARMED`, `ARMED`, `ALARM`
Comandos: `arm`, `disarm`, `silence`, `lock`, `unlock`

## MQTT

Broker: `broker.hivemq.com:1883`
Base: `ds8/security/<device_id>`

| Tópico | Payload |
|---|---|
| `/telemetry` | `{"motion":1,"distance":35.2,"door":0,"state":"ARMED"}` |
| `/events` | `{"type":"intrusion","sensor":"pir"}` |
| `/commands` | `{"id":12,"action":"arm"}` |
| `/ack` | `{"id":12,"result":"ok"}` |

## Base de datos (SQLite)

| Tabla | Columnas |
|---|---|
| `readings` | id, motion, distance, door, state, timestamp |
| `events` | id, type, sensor, timestamp |
| `commands` | id, action, source, result, timestamp |

## ThingSpeak

| Campo | Dato |
|---|---|
| field1 | motion |
| field2 | distance |
| field3 | door |
| field4 | state (0, 1, 2) |

Comandos desde la nube: TalkBack.
