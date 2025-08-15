# Arquitectura del Sistema

## Componentes principales
- Microcontrolador: Raspberry Pi Pico (RP2040)
- Sensores:
  - BME280 (I2C): temperatura, humedad relativa, presión
  - Sensor de humedad de suelo (ADC interno o ADS1115)
- ADC externo (opcional): ADS1115 (1 o 2 unidades) vía I2C
- Indicadores LED:
  - Por planta: 3 LEDs para 1-4 plantas y 2 LEDs para 4-8 plantas
  - De sistema: Encendido y Comunicación API
  - Puede ser 1 LED RGB o 3 LEDs independientes.
- Conectividad: Wi‑Fi (en Pico W) para sincronización con API

## Componentes opcionales

Estos componentes se pueden añadir de forma opcional e independiente.

- Motor de riego
- Humidificador
- Control de luz
- Batería y placa solar
- VEML6075 o VEML7000 (I2C) Sensor de luz
- Ventilador

## Modos de despliegue
- 1 planta: ADC interno de la Pico
- 1–4 plantas: 1× ADS1115 por I2C
- 4–8 plantas: 2× ADS1115 por I2C (direcciones distintas)

## Flujo de datos
1. Lectura de sensores (suelo + BME280 + VEML6075 o VEML7000)
2. Procesamiento y evaluación de estados por planta
3. Actualización de LEDs por planta y de sistema
4. Sincronización con API (descarga de configuración y envío de lecturas)
5. Ciclo de espera según intervalo configurado (deepsleep)

## Consideraciones técnicas
- Gestión de energía: patrones de LED y modos de bajo consumo
- Escalabilidad: indicadores simplificados para 2–8 plantas
- Robustez: secuencias de error mediante LEDs y reintentos en red

## Separación de responsabilidades (propuesta)
- Models/System.py: control de sistema y energía
- Models/RpiPico.py: HAL/abstracción de hardware (I2C, SPI, ADC, Wi‑Fi)
- Models/Sensors/*: drivers de sensores (BME280, SoilMoisture, VEML6075, VEML7000)
- Models/ADS1115.py: driver del ADC externo
- Models/Api.py: comunicación y formatos con la API
- Models/Plant.py: lógica de planta (umbrales, estados)
- Models/Location.py: datos de ubicación/tiempo recibidos de la API
- Models/System.py Entidad para agrupar todos los datos de las plantas y el 
  sistema de control general.

Consulta docs/operation.md para estados operativos y docs/api.md para formatos de API.
