# Proyecto SmartPlant (Hardware con Raspberry Pi Pico)

## Análisis de Pines para Configuración Mixta

### Configuración 1 Planta

- **LEDs por planta**: 3 pines GPIO (Rojo/Verde/Amarillo)
- **I2C (BME280)**: 2 pines GPIO
- **Sensor humedad suelo**: 1 pin ADC (analógico interno)
- **Monitorización batería**: 1 pin ADC (opcional)
- **LED sistema encendido**: 1 pin GPIO
- **LED subida API**: 1 pin GPIO

**Total 1 planta**: 8 pines GPIO + 2 pines ADC = **10 pines totales** 
### Configuración 8 Plantas

- **LEDs por planta**: 2 pines GPIO × 8 = 16 pines GPIO (Verde/Rojo)
- **I2C (BME280 + ADS1115)**: 2 pines GPIO
- **Monitorización batería**: 1 pin ADC
- **LED sistema encendido**: 1 pin GPIO
- **LED subida API**: 1 pin GPIO

**Total 8 plantas**: 20 pines GPIO + 1 pin ADC = **21 pines totales** 

# Sistema de Monitorización IoT para Plantas con Raspberry Pi Pico

## Descripción del Proyecto

Sistema de monitorización inteligente para el cuidado de plantas basado en Raspberry Pi Pico con MicroPython. El dispositivo recopila datos ambientales y de humedad del suelo, proporcionando indicadores visuales del estado de salud de las plantas y comunicación con API externa para configuración y almacenamiento de datos.

## Especificaciones de Hardware

### Componentes Principales
- **Microcontrolador**: Raspberry Pi Pico (RP2040)
- **Sensor de humedad del suelo**: Sensor capacitivo resistente a la corrosión (GND, VCC, A0)
- **Sensor ambiental**: Bosch BME280 (temperatura, humedad relativa, presión atmosférica)
- **Indicadores de planta**: LEDs individuales para estado de cada planta
- **LEDs de sistema**: LED de encendido y LED de comunicación API
- **Conectores**: JST para conexiones modulares

### Componentes según Configuración

#### Configuración Individual (1 Planta)
- **LEDs por planta**: 3 LEDs individuales (Rojo/Verde/Amarillo)
- **Sensor de humedad**: ADC interno de la Raspberry Pi Pico
- **Conectores JST**:
  - 4 pines para I2C (VCC, GND, SDA, SCL)
  - 3 pines para sensor analógico (VCC, GND, A0)
  - 5 pines para LEDs de planta (GND, R, G, Y, VCC)
  - 3 pines para LEDs de sistema (GND, Power, API, VCC)

#### Configuración Múltiple (hasta 8 Plantas)
- **LEDs por planta**: 2 LEDs individuales (Verde/Rojo)
  - Verde: Condiciones óptimas
  - Rojo: Requiere atención (incluye advertencia y crítico)
- **ADC externo**: Módulo ADS1115 de 16 bits vía I2C
- **Conectores JST**:
  - 4 pines para I2C principal (VCC, GND, SDA, SCL)
  - 3 pines por sensor (hasta 4 por ADS1115)
  - 4 pines para LEDs por planta (GND, G, R, VCC)
  - 3 pines para LEDs de sistema (GND, Power, API, VCC)

### Componentes de Sistema
- **LED de encendido**: Indica que el microcontrolador está funcionando
- **LED de comunicación API**: Indica actividad de subida/descarga de datos
- **Monitorización de batería**: Circuito divisor de tensión (opcional)
- **Panel solar**: Módulo de 80x50mm o 50x30mm para alimentación autónoma (opcional)

## Asignación de Pines (Pinout)

### Configuración Individual (1 Planta)

Comunicación:

- BME280 (I2C): SDA → GPIO 4, SCL → GPIO 5

Sensores:

- Sensor humedad suelo: A0 → GPIO 26 (ADC0)
- Monitorización batería: GPIO 27 (ADC1) - Opcional

LEDs de Planta:

- LED Verde (Planta): GPIO 16
- LED Amarillo (Planta): GPIO 17
- LED Rojo (Planta): GPIO 18

LEDs de Sistema:

- LED Encendido: GPIO 19
- LED Comunicación API: GPIO 20

Pines utilizados: 8 GPIO + 2 ADC

| Función                 | Componente         | Pin Pico       | Tipo           |
| ----------------------- | ------------------ | -------------- | -------------- |
| I2C SDA                 | BME280             | GPIO 4         | I2C SDA        |
| I2C SCL                 | BME280             | GPIO 5         | I2C SCL        |
| Sensor humedad suelo    | Sensor capacitivo  | GPIO 26 (ADC0) | ADC            |
| Monitorización batería  | Divisor de tensión | GPIO 27 (ADC1) | ADC (opcional) |
| LED Verde (planta)      | LED                | GPIO 16        | GPIO           |
| LED Amarillo (planta)   | LED                | GPIO 17        | GPIO           |
| LED Rojo (planta)       | LED                | GPIO 18        | GPIO           |
| LED Encendido (sistema) | LED                | GPIO 19        | GPIO           |
| LED Comunicación API    | LED                | GPIO 20        | GPIO           |

### Configuración Múltiple (8 Plantas)

Comunicación:

- BME280 + ADS1115 (I2C): SDA → GPIO 4, SCL → GPIO 5

Sensores:

- Sensores humedad: A0-A3 del ADS1115 (plantas 1-4)
- Segundo ADS1115: A0-A3 (plantas 5-8) - Opcional
- Monitorización batería: GPIO 26 (ADC0)

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

|Función|Componente|Pin Pico|Tipo|
|---|---|---|---|
|I2C SDA|BME280 + ADS1115|GPIO 4|I2C SDA|
|I2C SCL|BME280 + ADS1115|GPIO 5|I2C SCL|
|Monitorización batería|Divisor de tensión|GPIO 26 (ADC0)|ADC|
|LED Encendido (sistema)|LED|GPIO 6|GPIO|
|LED Comunicación API|LED|GPIO 7|GPIO|


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


## Sistema de Indicadores Visuales

### LEDs de Planta

#### Configuración Individual (3 LEDs)
- **Verde**: Condiciones óptimas (humedad del suelo en rango ideal)
- **Amarillo**: Condiciones de advertencia (fuera del rango óptimo)
- **Rojo**: Condiciones críticas (requiere intervención inmediata)

#### Configuración Múltiple (2 LEDs)
- **Verde**: Condiciones óptimas (humedad del suelo en rango ideal)
- **Rojo**: Requiere atención (combina advertencia y crítico)
- **Alternado Verde/Rojo**: Condiciones de advertencia (parpadeo)
- **Rojo fijo**: Condiciones críticas

### LEDs de Sistema
- **LED Encendido**: 
  - Encendido fijo: Sistema funcionando correctamente
  - Parpadeo lento: Modo de bajo consumo
  - Apagado: Sistema sin alimentación o error crítico

- **LED Comunicación API**:
  - Parpadeo rápido: Comunicando con API
  - Encendido breve: Datos enviados correctamente
  - Parpadeo lento: Error de comunicación
  - Apagado: Sin actividad de red

## Funcionalidades del Sistema

### Monitorización de Sensores
- **Humedad del suelo**: Lectura cada 30 minutos (configurable vía API)
- **Condiciones ambientales**: Temperatura, humedad relativa y presión atmosférica
- **Estado de batería**: Monitorización del nivel de carga (opcional)
- **Calibración automática**: Ajuste de rangos según tipo de planta

### Comunicación API
- **Configuración inicial**: Descarga de parámetros específicos del dispositivo
- **Sincronización de datos**: Envío de lecturas con identificador único (device_id)
- **Gestión de errores**: Reintento automático en caso de fallos de comunicación
- **Configuración remota**: Actualización de intervalos de lectura y rangos de alerta
- **Indicación visual**: LED de comunicación muestra estado de conectividad

### Estados de Funcionamiento

#### Secuencia de Inicio
1. **LED Encendido** se activa (sistema iniciando)
2. **LED API** parpadea durante descarga de configuración
3. **LEDs de plantas** realizan secuencia de prueba
4. Sistema entra en modo de monitorización normal

#### Ciclo de Monitorización
1. Lectura de sensores (LED Encendido parpadea)
2. Procesamiento de datos y actualización de LEDs de plantas
3. Envío a API (LED API activo)
4. Período de espera hasta próximo ciclo

## Consideraciones Técnicas

### Gestión de Energía
- LEDs de sistema optimizados para bajo consumo
- Reducción de brillo en modo nocturno (configurable)
- Modo hibernación con indicadores mínimos

### Escalabilidad
- **1 planta**: Máximo detalle en indicadores (3 estados)
- **2-8 plantas**: Indicadores simplificados pero eficientes (2 estados + parpadeo)
- Configuración automática según número de plantas detectadas

### Robustez del Sistema
- LEDs de sistema permiten diagnóstico visual sin necesidad de herramientas
- Secuencias de parpadeo para diferentes tipos de error
- Recuperación automática de errores de comunicación

## Configuraciones Recomendadas

### Para Uso Doméstico (1-2 plantas)
- Configuración individual con 3 LEDs por planta
- Máxima precisión en indicadores visuales
- Ideal para plantas de interior de alto valor

### Para Jardín o Huerto (3-8 plantas)
- Configuración múltiple con 2 LEDs por planta
- Monitorización eficiente de múltiples plantas
- Sistema de alertas centralizado

## Propuestas de Mejora Futura

### Hardware
- **Buzzer opcional**: Alertas sonoras para condiciones críticas
- **Sensor de luz**: Ajuste automático de brillo de LEDs
- **Display OLED**: Información detallada local (alternativa a múltiples LEDs)

### Software
- **Patrones de parpadeo personalizables**: Diferentes secuencias según preferencias
- **Modo silencioso**: Desactivación de LEDs durante horas nocturnas
- **Diagnóstico automático**: Detección de LEDs defectuosos

## Notas de Implementación

La elección entre configuración individual o múltiple debe realizarse al inicio del proyecto según las necesidades específicas:

- **Jardines pequeños/plantas premium**: Configuración individual
- **Huertos/jardines extensos**: Configuración múltiple
- **Uso mixto**: Posibilidad de combinar ambas configuraciones en proyectos futuros
