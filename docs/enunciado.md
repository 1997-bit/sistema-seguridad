# Parcial #2 Desarrollo de Software VIII: Sistema IoT de Monitoreo y Control Inteligente

Valor: 100 puntos.

Desarrollarán un Sistema IoT completo que simule un entorno de monitoreo y control inteligente utilizando el simulador Wokwi, sensores, actuadores y una plataforma en la nube. El sistema debe recopilar datos, almacenarlos, procesarlos y permitir control remoto bidireccional.

## Escenario a implementar (elijan uno)

1. Smart Home - Sistema de automatización del hogar
2. Invernadero Inteligente - Control de condiciones de cultivo
3. Estación Meteorológica - Monitoreo ambiental
4. Sistema de Seguridad - Detección y alertas
5. Monitoreo Industrial - Control de variables de producción de un producto "x"

## Requisitos

- Mínimo 2 sensores diferentes (temperatura, humedad, luz, movimiento, distancia, etc.)
- Mínimo 2 actuadores (LEDs, buzzer, motor, relay, display LCD/OLED)
- Código en Python modular y bien documentado
- Manejo de GPIO usando librerías apropiadas
- Lectura de sensores en tiempo real
- Control de actuadores
- Implementar cliente MQTT en el dispositivo (HiveMQ, Mosquitto o EMQX Cloud gratuito)
- Conectar con una base de datos (SQLite local o MySQL/PostgreSQL remota):
  - Almacenar lecturas de sensores con timestamp
  - Registrar eventos y comandos ejecutados
  - Implementar consultas para recuperar históricos
- Plataforma en la nube, usar una de estas opciones: ThingSpeak (recomendado para comenzar), Adafruit IO, AWS, Azure IoT Hub, Google Cloud IoT:
  - Dashboard de visualización en tiempo real
  - Recepción de comandos desde la nube hacia el dispositivo
- Programación modular y orientada a eventos

## Entregables

- Código fuente debidamente estructurado en GitHub y en Teams. Incluir README, requirements.txt (especificar los que aportaron en el desarrollo del examen), archivos con los scripts SQL, diagrama de la arquitectura, capturas del circuito y el proyecto zip generado por Wokwi.
- Documentación de la arquitectura IoT, diagrama de flujo de datos, configuración de la plataforma cloud.
- Sustentación oral.

## Criterios de evaluación

| Aspecto | Peso |
|---|---|
| Funcionamiento completo del sistema | 30% |
| Calidad del código (estructura, comentarios, buenas prácticas) | 10% |
| Integración exitosa de todos los componentes | 5% |
| Documentación | 5% |
| Sustentación | 50% |
