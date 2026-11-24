# Arquitectura

El Pico W publica por MQTT a HiveMQ y a Adafruit IO. La PC escucha HiveMQ y guarda en MariaDB. Los comandos llegan desde Adafruit, HiveMQ o el botón.

## Componentes

- **Pico W (Wokwi)**: lee los sensores, maneja la alarma y los actuadores, y habla MQTT con HiveMQ y Adafruit IO
- **HiveMQ**: broker MQTT público, recibe telemetría, eventos y ack, y manda comandos
- **Adafruit IO**: nube con el dashboard en tiempo real y los botones para mandar comandos
- **registrador.py**: corre en la PC, escucha HiveMQ y guarda todo en MariaDB
- **MariaDB (XAMPP)**: base `seguridad` con las tablas `lecturas`, `eventos` y `comandos`

## Diagrama de arquitectura

```mermaid
flowchart LR
    subgraph Wokwi
        PIR[PIR] --> Pico
        HC[HC-SR04] --> Pico
        BTN[Botón] --> Pico
        Pico[Pico W] --> LED[LED RGB]
        Pico --> BUZ[Buzzer]
        Pico --> LCD[LCD 16x2]
    end

    Pico <-->|MQTT| HiveMQ[(HiveMQ)]
    Pico <-->|MQTT| AIO[Adafruit IO]

    subgraph PC
        REG[registrador.py] --> DB[(MariaDB)]
    end

    HiveMQ -->|telemetry, events, ack| REG
    AIO --- DASH[Dashboard]
```

## Flujo de datos

### Telemetría e intrusión

Cada lectura y cada intrusión termina en MariaDB. Adafruit solo recibe un resumen cada 10 s por su límite de 30 datos/min.

```mermaid
sequenceDiagram
    participant S as Sensores
    participant P as Pico W
    participant H as HiveMQ
    participant R as registrador.py
    participant D as MariaDB
    participant A as Adafruit IO

    loop cada 1 s
        S->>P: movimiento y distancia
        P->>H: ds8/security/pico1/telemetry
        H->>R: lectura
        R->>D: INSERT en lecturas
    end
    loop cada 10 s
        P->>A: feeds movimiento, distancia, estado
    end
    Note over P: si está ARMADO y hay intrusión, pasa a ALARMA
    P->>H: ds8/security/pico1/events
    H->>R: evento
    R->>D: INSERT en eventos
```

### Comandos

Venga de donde venga, el comando se ejecuta en el Pico y su `ack` se guarda en la tabla `comandos`.

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as Adafruit IO
    participant H as HiveMQ
    participant P as Pico W
    participant R as registrador.py
    participant D as MariaDB

    alt desde Adafruit
        U->>A: botón del dashboard
        A->>P: feed comandos
    else desde HiveMQ
        U->>H: ds8/security/pico1/commands
        H->>P: comando
    else desde el circuito
        U->>P: botón físico
    end
    P->>P: ejecuta armar, desarmar o silenciar
    P->>H: ds8/security/pico1/ack
    H->>R: ack
    R->>D: INSERT en comandos
```

## Estados de la alarma

Solo dispara si está ARMADO. `desarmar` siempre vuelve a DESARMADO.

```mermaid
stateDiagram-v2
    [*] --> DESARMADO
    DESARMADO --> ARMADO: armar
    ARMADO --> ALARMA: PIR o distancia < 100 cm
    ALARMA --> ALARMA: silenciar (apaga buzzer)
    ARMADO --> DESARMADO: desarmar
    ALARMA --> DESARMADO: desarmar
```
