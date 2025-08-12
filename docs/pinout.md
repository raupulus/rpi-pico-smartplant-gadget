# Pinout y Asignación de Pines

Esta sección resume la asignación de pines para las distintas configuraciones del sistema.







## TODO: Encontrar un pin libre para el ventilador
## TODO: Encontrar pines libres que pueda utilizar en el modo 4 plantas con 1xADS1115
## TODO: Añadir detector de agua mediante interruptor magnético con boya







## 1 planta (configuración individual)

Comunicación:
- BME280 (I2C): SDA → GPIO 4, SCL → GPIO 5
- VEML6075 o VEML6070 (I2C): SDA → GPIO 4, SCL → GPIO 5
- Ventilador (DIGITAL): GPIO ??
- Control luz parainterior (DIGITAL): GPIO ??

Sensores:
- Sensor humedad suelo: A0 → GPIO 27 (ADC1)
- Monitorización batería: GPIO 26 (ADC0) – opcional
- Sensor nivel de agua (boya): GPIO 23 – opcional

LEDs de Planta:
- LED Verde (Planta): GPIO 16
- LED Azul (Planta): GPIO 17
- LED Rojo (Planta): GPIO 18

LEDs de Sistema:
- LED Encendido: GPIO 19
- LED Comunicación API: GPIO 20

Pines utilizados: 8 GPIO + 2 ADC

| Función                 | Componente         | Pin Pico       | Tipo           |
|-------------------------| ------------------ |----------------| -------------- |
| I2C SDA                 | BME280             | GPIO 4         | I2C SDA        |
| I2C SCL                 | BME280             | GPIO 5         | I2C SCL        |
| Sensor humedad suelo    | Sensor capacitivo  | GPIO 26 (ADC0) | ADC            |
| Monitorización batería  | Divisor de tensión | GPIO 27 (ADC1) | ADC (opcional) |
| Sensor nivel de agua    | Boya/switch        | GPIO 23        | GPIO (opcional) |
| LED Verde (planta)      | LED                | GPIO 16        | GPIO           |
| LED Azul (planta)       | LED                | GPIO 17        | GPIO           |
| LED Rojo (planta)       | LED                | GPIO 18        | GPIO           |
| LED Encendido (sistema) | LED                | GPIO 19        | GPIO           |
| LED Comunicación API    | LED                | GPIO 20        | GPIO           |
| Control bomba de agua   | Relé/MOSFET driver | GPIO 21        | GPIO (opcional)|
| Control luz interior    | Relé/MOSFET driver | GPIO 22        | GPIO (opcional)|
| Ventilador              | Relé/MOSFET driver | GPIO ??        | GPIO (opcional)|


> Nota (LED RGB 4 pines): si en lugar de 3 LEDs individuales se utiliza un LED RGB de 4 pines, las resistencias pueden ser: Rojo 680R, Azul 680R y Verde 20k para reducir brillo y consumo. La opción de LEDs individuales sigue siendo totalmente válida y soportada.

## 1-4 planta (configuración múltiple con 1xADS1115)

Igual que para una planta individual, pero con un ADS1115 adicional y usando
más GPIO para los leds por cada planta:

- Planta 1: GPIO 8 (G), GPIO 9 (R), GPIO ?? (B)
- Planta 2: GPIO 10 (G), GPIO 11 (R), GPIO ?? (B)
- Planta 3: GPIO 12 (G), GPIO 13 (R), GPIO ?? (B)
- Planta 4: GPIO 14 (G), GPIO 15 (R), GPIO ?? (B)


## 8 plantas (configuración múltiple con 2xADS1115)

Comunicación:
- BME280 + ADS1115 (I2C): SDA → GPIO 4, SCL → GPIO 5

Sensores:
- Sensores humedad en tierra: A0–A3 del ADS1115 (plantas 1–4)
- Segundo ADS1115: A0–A3 (plantas 5–8) – opcional
- Monitorización batería: GPIO 26 (ADC0)
- Sensor nivel de agua (boya): GPIO 2 – opcional

LEDs de Plantas (Verde/Rojo):
- Planta 1: GPIO 8 (G), GPIO 9 (R)
- Planta 2: GPIO 10 (G), GPIO 11 (R)
- Planta 3: GPIO 12 (G), GPIO 13 (R)
- Planta 4: GPIO 14 (G), GPIO 15 (R)
- Planta 5: GPIO 16 (G), GPIO 17 (R)
- Planta 6: GPIO 18 (G), GPIO 19 (R)
- Planta 7: GPIO 20 (G), GPIO 21 (R)
- Planta 8: GPIO 22 (G), GPIO 27 (R)

LEDs de Sistema:
- LED Encendido: GPIO 6
- LED Comunicación API: GPIO 7

Pines utilizados: 20 GPIO + 1 ADC

| Función                 | Componente                           | Pin Pico       |Tipo|
|-------------------------|--------------------------------------|----------------|---|
| I2C SDA                 | BME280 + ADS1115 + VEML6075/VEML7000 | GPIO 4         |I2C SDA|
| I2C SCL                 | BME280 + ADS1115 + VEML6075/VEML7000                     | GPIO 5         |I2C SCL|
| Monitorización batería  | Divisor de tensión                   | GPIO 26 (ADC0) |ADC|
| Sensor nivel de agua    | Boya/switch                          | GPIO 2         |GPIO (opcional)|
| LED Encendido (sistema) | LED                                  | GPIO 6         |GPIO|
| LED Comunicación API    | LED                                  | GPIO 7         |GPIO|
| Control bomba de agua   | Relé/MOSFET driver                   | GPIO 0         |GPIO (opcional)|
| Control luz interior    | Relé/MOSFET driver                   | GPIO 1         |GPIO (opcional)|
| Ventilador              | Relé/MOSFET driver                   | GPIO ??????    |GPIO (opcional)|

|Planta|LED Verde (GPIO)|LED Rojo (GPIO)|
|---|---|---|
|1|GPIO 8|GPIO 9|
|2|GPIO 10|GPIO 11|
|3|GPIO 12|GPIO 13|
|4|GPIO 14|GPIO 15|
|5|GPIO 16|GPIO 17|
|6|GPIO 18|GPIO 19|
|7|GPIO 20|GPIO 21|
|8|GPIO 22|GPIO 27|

Consulta [docs/hardware.md](docs/hardware.md) para detalles de conectores y [docs/operation.md](docs/operation.md) para la semántica de LEDs.
