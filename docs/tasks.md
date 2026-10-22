# Tareas

| Quién | Qué | Archivos |
|---|---|---|
| Arles | Circuito + sensores + capturas | `wokwi/diagram.json`, `wokwi/config.py`, `wokwi/sensors.py`, `docs/screenshots/` |
| Gloria | Actuadores + alarma + main + zip Wokwi | `wokwi/actuators.py`, `wokwi/alarm.py`, `wokwi/main.py` |
| Luis | MQTT + bridge + diagramas | `wokwi/mqtt_client.py`, `gateway/bridge.py`, `docs/architecture.md` |
| Juan | Base de datos + ThingSpeak | `sql/`, `gateway/database.py`, `gateway/thingspeak.py`, `docs/cloud.md` |
| Alex | README + requirements | `README.md`, `requirements.txt` |


## Git

```bash
git clone https://github.com/1997-bit/sistema-seguridad.git
git checkout -b feature/<nombre>
git add . && git commit -m "mensaje"
git push -u origin feature/<nombre>
```

