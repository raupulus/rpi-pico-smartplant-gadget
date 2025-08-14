# Pinout y Asignación de Pines

Esta sección resume la asignación de pines para las distintas configuraciones del sistema.

## Pines Fijos (Comunes a todas las configuraciones)

Los siguientes pines se mantienen constantes en todas las configuraciones:

| Función | Pin | Tipo | Descripción |
|---------|-----|------|-------------|
| Bomba de agua | GPIO 0 | GPIO | Control riego |
| Control luz interior | GPIO 1 | GPIO | Control iluminación interior |
| Nivel de agua | GPIO 2 | GPIO | Detector con boya magnética |
| Ventilador | GPIO 3 | GPIO | Control de ventilador con relé/MOSFET |
| I2C SDA | GPIO 4 | I2C | Comunicación con BME280, ADS1115, VEML |
| I2C SCL | GPIO 5 | I2C | Comunicación con BME280, ADS1115, VEML |
| LED Sistema (Power) | GPIO 6 | GPIO | Indicador encendido del sistema |
| LED Sistema (API) | GPIO 7 | GPIO | Indicador comunicación API |
| Humidificador | GPIO 8 | GPIO | Control de humidificador con relé/MOSFET |
| Batería | GPIO 26 (ADC0) | ADC | Monitorización nivel de batería |

> **Nota importante:** Los pines GPIO 23-25 están reservados para WiFi/Bluetooth en la Raspberry Pi Pico W y no pueden ser utilizados.

## 1 planta (configuración individual)

Esta configuración utiliza el ADC interno de la Raspberry Pi Pico W para medir la humedad del suelo.

**Pines utilizados: 12 GPIO + 2 ADC = 14 pines**

| Función                 | Componente         | Pin Pico       | Tipo           |
|-------------------------| ------------------ |----------------| -------------- |
| Control bomba de agua   | Relé/MOSFET driver | GPIO 0         | GPIO (opcional)|
| Control luz interior    | Relé/MOSFET driver | GPIO 1         | GPIO (opcional)|
| Sensor nivel de agua    | Boya/switch        | GPIO 2         | GPIO (opcional) |
| Ventilador              | Relé/MOSFET driver | GPIO 3         | GPIO (opcional)|
| I2C SDA                 | BME280, VEML       | GPIO 4         | I2C SDA        |
| I2C SCL                 | BME280, VEML       | GPIO 5         | I2C SCL        |
| LED Sistema (Power)     | LED                | GPIO 6         | GPIO           |
| LED Sistema (API)       | LED                | GPIO 7         | GPIO           |
| Humidificador           | Relé/MOSFET driver | GPIO 8         | GPIO (opcional)|
| LED Verde (planta)      | LED                | GPIO 9         | GPIO           |
| LED Azul (planta)       | LED                | GPIO 10        | GPIO           |
| LED Rojo (planta)       | LED                | GPIO 11        | GPIO           |
| Sensor humedad suelo    | Sensor capacitivo  | GPIO 27 (ADC1) | ADC            |
| Monitorización batería  | Divisor de tensión | GPIO 26 (ADC0) | ADC (opcional) |


> Nota (LED RGB 4 pines): si en lugar de 3 LEDs individuales se utiliza un LED RGB de 4 pines, las resistencias pueden ser: Rojo 680R, Azul 680R y Verde 20k para reducir brillo y consumo. La opción de LEDs individuales sigue siendo totalmente válida y soportada.

## 1-4 plantas (configuración múltiple con 1x ADS1115)

Esta configuración utiliza un módulo ADS1115 externo para leer hasta 4 sensores de humedad del suelo simultaneamente. Permite monitorizar de 1 a 4 plantas con LEDs RGB completos para cada una.

**Pines utilizados: 22 GPIO + 1 ADC = 23 pines**

> Los pines comunes del sistema (I2C, batería, agua, ventilador, LEDs sistema, bomba, luz) están definidos en la sección "Pines Fijos" arriba.

**LEDs por Planta (RGB completo):**
| Planta | LED Verde | LED Rojo | LED Azul |
|--------|-----------|----------|----------|
| Planta 1 | GPIO 12 | GPIO 13 | GPIO 14 |
| Planta 2 | GPIO 15 | GPIO 16 | GPIO 17 |
| Planta 3 | GPIO 18 | GPIO 19 | GPIO 20 |
| Planta 4 | GPIO 21 | GPIO 22 | GPIO 27 |


## 4-8 plantas (configuración múltiple con 2x ADS1115)

Esta configuración utiliza dos módulos ADS1115 externos para leer hasta 8 sensores de humedad del suelo simultaneamente. Para maximizar el número de plantas, se utilizan solo LEDs Verde y Rojo por planta (sin azul).

**Pines utilizados: 25 GPIO + 1 ADC = 26 pines**

> Los pines comunes del sistema (I2C, batería, agua, ventilador, LEDs sistema, bomba, luz) están definidos en la sección "Pines Fijos" arriba.

### LEDs por Planta (Verde/Rojo solamente)

| Planta | LED Verde | LED Rojo |
|--------|-----------|----------|
| Planta 1 | GPIO 9 | GPIO 10 |
| Planta 2 | GPIO 11 | GPIO 12 |
| Planta 3 | GPIO 13 | GPIO 14 |
| Planta 4 | GPIO 15 | GPIO 16 |
| Planta 5 | GPIO 17 | GPIO 18 |
| Planta 6 | GPIO 19 | GPIO 20 |
| Planta 7 | GPIO 21 | GPIO 22 |
| Planta 8 | GPIO 27 | GPIO 28 |

> **Nota:** GPIO 27 y GPIO 28 pueden usarse como GPIO digitales aunque sean pines ADC. El humidificador está ahora en GPIO 8. Los LEDs azules se omiten para optimizar el uso de pines.

Consulta [docs/hardware.md](docs/hardware.md) para detalles de conectores y [docs/operation.md](docs/operation.md) para la semántica de LEDs.
