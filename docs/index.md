# Documentación del Proyecto SmartPlant (Raspberry Pi Pico)

Bienvenido/a a la documentación del proyecto SmartPlant. Este sitio reúne toda la información necesaria para planificar, implementar y mantener el dispositivo de monitorización de plantas basado en Raspberry Pi Pico con MicroPython.

## Índice
- Visión general: overview.md
- Requisitos e instalación: setup.md
- Requisitos técnicos detallados: requeriments.md
- Hardware y conexiones: hardware.md
- Pinout y asignación de pines: pinout.md
- Arquitectura y consideraciones: architecture.md
- Operación y estados (LEDs, ciclos): operation.md
- Comunicación con la API: api.md
- Configuración del entorno (env.py): env.md
- Hoja de ruta (roadmap): roadmap.md

## Contextos de uso
- 1 planta: usa el ADC interno de la Raspberry Pi Pico
- 1–4 plantas: usa un ADC externo ADS1115 por I2C
- 4–8 plantas: usa dos ADC externos ADS1115 por I2C

## Licencia
Este proyecto está licenciado bajo GPLv3. Consulta LICENSE para más detalles.
