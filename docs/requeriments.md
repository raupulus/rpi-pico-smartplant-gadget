# Requisitos detallados

## Software
- MicroPython: 1.26 (en la Raspberry Pi Pico/Pico W)
- IDE/Editor recomendado: Thonny, PyCharm, VS Code
- Python (en el PC) para utilidades opcionales
- Sistema operativo en PC: Linux/macOS/Windows

## Hardware mínimo (1 planta)
- Raspberry Pi Pico (o Pico W para Wi‑Fi)
- 1× Sensor de humedad del suelo capacitivo (salida analógica)
- 1× Sensor BME280 (I2C)
- 3× LEDs (Verde, Azul, Rojo) + resistencias adecuadas
- Cables y conectores JST

## Hardware para 1–4 plantas
- Todo lo anterior, excepto:
  - 3 LEDs por planta (Verde/Azul/Rojo) + resistencias adecuadas
  - 1× ADS1115 (I2C) para 4 entradas analógicas

## Hardware para 4–8 plantas
- Igual que 1–4 plantas, más:
  - 2× ADS1115 (I2C) con direcciones distintas
  - LEDs por planta: 2 recomendados (Verde/Rojo) ya que no hay suficiente espacio para 3

## Opcionales
- Monitorización de batería (divisor de tensión a un pin ADC)
- Panel solar 80×50mm o 50×30mm
- Caja/soporte e impresiones 3D
- Ventilador
- Boya para sensor de agua
- Iluminación
- Bomba de agua
- Cacharro de agua
- Relé o mofset para iluminación/ventilador/bomba de agua

## Pines y conexiones
- Ver [docs/pinout.md](docs/pinout.md) para asignaciones concretas por modo
- Ver [docs/hardware.md](docs/hardware.md) para detalle de conectores y módulos

## Red y API
- Wi‑Fi configurado (Pico W) con SSID principal y alternativos
- URL de API, token y path configurados en env.py (ver docs/env.md)
