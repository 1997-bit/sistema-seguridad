# Sistema de Seguridad IoT

Parcial #2

Integrantes: Arles, Gloria, Luis, Juan, Alex.

| | |
|---|---|
| Placa | Raspberry Pi Pico W (Wokwi) |
| Sensores | PIR, HC-SR04, botón |
| Actuadores | LED RGB, buzzer, LCD 16x2 I2C |
| MQTT | HiveMQ (`broker.hivemq.com:1883`) |
| Nube | Adafruit IO |
| BD | MariaDB (XAMPP) |

![Circuito en Wokwi](docs/screenshots/wokwi.png)

## Cómo funciona

- Estados: `DESARMADO` (azul), `ARMADO` (verde), `ALARMA` (rojo + buzzer)
- Armado, el PIR o una distancia menor a 100 cm disparan la alarma
- Comandos: `armar`, `desarmar`, `silenciar`. Llegan por el botón, HiveMQ o Adafruit IO
- El Pico publica telemetría cada 1 s en HiveMQ y cada 10 s en Adafruit IO
- `gateway/logger.py` escucha HiveMQ en la PC y guarda todo en MariaDB

Tópicos y payloads en el [contrato](docs/contract.md).

## Estructura

| Carpeta | Qué tiene |
|---|---|
| `wokwi/` | Código del Pico W y circuito |
| `gateway/` | Logger MQTT → MariaDB |
| `sql/` | Esquema y consultas |
| `docs/` | Contrato, tareas, enunciado y capturas |

## Cómo correrlo

### Pico W (Wokwi)

1. Crear un proyecto Pico W MicroPython en Wokwi
2. Subir todos los archivos de `wokwi/`
3. En `secretos.py` poner usuario y key de Adafruit IO
4. En Adafruit IO crear los feeds `movimiento`, `distancia`, `estado` y `comandos`
5. Iniciar la simulación

### Base de datos

1. Iniciar Apache y MySQL en XAMPP
2. En phpMyAdmin importar `sql/schema.sql`
3. Crear el usuario `ds8` con clave `ds8` y permisos sobre `seguridad`

### Logger

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd gateway
python logger.py
```

## Probar comandos sin Adafruit

```bash
mosquitto_pub -h broker.hivemq.com -t ds8/security/pico1/commands -m armar
mosquitto_sub -h broker.hivemq.com -t "ds8/security/pico1/#" -v
```

## Docs

- [Contrato](docs/contract.md)
- [Tareas](docs/tasks.md)
- [Enunciado](docs/assignment.md)
