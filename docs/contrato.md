# Contrato

Nombres de funciones, tópicos, payloads, tablas y feeds que comparten el Pico, el registrador y la nube.

## Pines

Están en `wokwi/configuracion.py`.

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

## Base de datos (MariaDB)

| Tabla | Columnas |
|---|---|
| `lecturas` | id, fecha, movimiento, distancia, estado |
| `eventos` | id, fecha, tipo, sensor |
| `comandos` | id, fecha, accion, origen, resultado |

## Adafruit IO

| Feed | Dato |
|---|---|
| `movimiento` | 0 o 1 |
| `distancia` | cm |
| `estado` | DESARMADO, ARMADO o ALARMA |
| `comandos` | armar, desarmar o silenciar (desde el dashboard) |
