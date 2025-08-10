# Visión General

SmartPlant es un sistema de monitorización inteligente para el cuidado de plantas basado en Raspberry Pi Pico y MicroPython. Recopila datos ambientales (temperatura, humedad relativa, presión) y de humedad del suelo, mostrando indicadores visuales (LEDs) del estado de cada planta y sincronizando datos con una API externa.

## Objetivos
- Monitorizar 1, 1–4 o 4–8 plantas reutilizando el mismo software según el hardware disponible.
- Permitir configuración remota desde la API (intervalos, rangos óptimos, preferencias de riego).
- Proveer diagnóstico visual mediante LEDs de planta y de sistema.
- Optimizar el consumo energético y soportar alimentación por batería/solar.

## Contextos de uso
- 1 planta: usa el ADC interno de la Raspberry Pi Pico.
- 1–4 plantas: usa un ADC externo ADS1115 por I2C.
- 4–8 plantas: usa dos ADC externos ADS1115 por I2C en paralelo.

## Estado del Proyecto
El proyecto está en fase de diseño y separación de responsabilidades. El código existente es una plantilla base para MicroPython sobre la que se implementarán las funcionalidades.

Consulta el índice general en docs/index.md para profundizar en cada sección.
