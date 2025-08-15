# Requisitos e Instalación

## Requisitos de software
- MicroPython 1.26 en Raspberry Pi Pico/Pico W.
- Editor/IDE: Thonny, PyCharm, VS Code, etc.
- (Opcional) Python en tu PC para herramientas auxiliares.

## Requisitos de hardware mínimo
- Raspberry Pi Pico (o Pico W para conectividad Wi‑Fi).
- Sensor BME280 (I2C) para temperatura, humedad y presión.
- Sensor de humedad de suelo (capacitivo analógico).
- LEDs para indicadores (planta y sistema) y resistencias adecuadas.
- (Opcional) ADS1115 por I2C (1 o 2 unidades) para múltiples plantas.
- Cables, conectores JST, protoboard, etc.

Consulta también [docs/requeriments.md](requeriments.md) para un listado detallado.

## Instalación
1. Clona o descarga este repositorio.
2. Crea el archivo env.py a partir de la plantilla y rellena los campos necesarios (Wi‑Fi, API, device_id). Consulta [docs/env.md](env.md) para ver el detalle de cada campo.
3. Copia todos los archivos dentro de la carpeta src/ a tu Raspberry Pi Pico.
4. Reinicia la Pico y verifica logs/LEDs de estado.

## Configuración según número de plantas
- 1 planta: usa el ADC interno (GPIO 27/ADC1) para el sensor de suelo.
- 1–4 plantas: usa un ADS1115 por I2C y asigna cada sensor a A0–A3.
- 4–8 plantas: usa dos ADS1115 con direcciones distintas por I2C.

## Enlaces útiles
- Pinout y asignación de pines: [docs/pinout.md](pinout.md)
- Arquitectura y flujo: [docs/architecture.md](architecture.md)
- Operación (LEDs y ciclos): [docs/operation.md](operation.md)
- Comunicación con la API: [docs/api.md](api.md)
- Visión general: [docs/overview.md](overview.md)
