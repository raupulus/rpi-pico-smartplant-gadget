# Configuración del entorno (env.py)

El archivo env.py define credenciales y preferencias de ejecución. No lo subas con datos reales a repositorios públicos. Mantén una plantilla local (p. ej. src/.env.example.py) y copia su contenido a env.py en tu entorno.

## Variables disponibles
- HOSTNAME: nombre del equipo (visible en la red Wi‑Fi).
- AP_NAME: SSID principal de la red Wi‑Fi.
- AP_PASS: contraseña del SSID principal.
- ALTERNATIVES_AP: lista de AP alternativos, por ejemplo [{"ssid": "...", "password": "..."}].

API
- API_URL: URL base de la API (https://.../api).
- API_TOKEN: token de autenticación (Bearer).
- API_UPLOAD: habilita el envío periódico de datos (True/False).
- API_UPLOAD_INTERVAL: intervalo entre subidas a la API (minutos).

Batería (opcional)
- BATTERY: habilita la monitorización de batería (True/False).
- BATTERY_PIN: pin GPIO para lectura de voltaje de batería (p. ej. 26).
- BATTERY_MIN_VOLTAGE: voltaje mínimo considerado 0% (p. ej. 2.7).
- BATTERY_MAX_VOLTAGE: voltaje máximo considerado 100% (p. ej. 4.15).

Calibración ADC para batería (opcional)
- BATTERY_DIVIDER_R1_OHMS: resistencia superior del divisor de voltaje (ohmios).
- BATTERY_DIVIDER_R2_OHMS: resistencia inferior del divisor de voltaje (ohmios).
- BATTERY_ADC_CALIBRATION_SCALE: factor de escala para calibración fina (1.0 por defecto).
- BATTERY_ADC_CALIBRATION_OFFSET: offset para calibración fina en voltios (0.0 por defecto).
- BATTERY_ESTIMATION_ALPHA: factor de suavizado EMA para estimar voltaje (0.1 por defecto).

Iluminación (opcional)
- LIGHT_CONTROL: habilita una salida GPIO para iluminación interior (True/False).
- LIGHT_CONTROL_PIN: GPIO que controla la iluminación (recomendado ver pinout.md).

Riego (opcional)
- WATERING_MOTOR: habilita control del motor/bomba de riego (True/False).
- WATERING_MOTOR_PIN: GPIO que activa el motor de agua.

Nivel de agua (opcional)
- WATER_LEVEL_SENSOR: habilita el sensor/boya de nivel de agua (True/False).
- WATER_LEVEL_SENSOR_PIN: GPIO que lee el estado del nivel de agua.

Control de múltiples plantas - ADS1115 (opcional)
- ADS1115: habilita el módulo ADC externo ADS1115 (True/False). Si es False, usa ADC interno de la RPi.
- ADS1115_ADDRESS: dirección I2C del primer módulo ADS1115 (p. ej. 0x48).
- ADS1115_QUANTITY: cantidad de plantas monitorizadas por el primer módulo (hasta 4).
- ADS1115_2: habilita un segundo módulo ADS1115 para hasta 8 plantas en total (True/False).
- ADS1115_2_ADDRESS: dirección I2C del segundo módulo ADS1115 (p. ej. 0x49).
- ADS1115_2_QUANTITY: cantidad de plantas monitorizadas por el segundo módulo (hasta 4).

Calibración de sensores de humedad del suelo (opcional)
- SOIL_DRY_VOLTAGE: voltaje medido cuando el suelo está seco (voltios, p. ej. 3.5).
- SOIL_WET_VOLTAGE: voltaje medido cuando el suelo está húmedo (voltios, p. ej. 1.8).
- SOIL_CALIBRATION_SCALE: escala de calibración para ajuste fino (1.0 por defecto).
- SOIL_CALIBRATION_OFFSET: offset de calibración en voltios (0.0 por defecto).
- SOIL_SAMPLES: número de muestras para promediar lecturas (8 por defecto).
- SOIL_SAMPLE_DELAY_MS: retardo entre muestras en milisegundos (5 por defecto).
- SOIL_ADS1115_PGA_FS: rango a plena escala del ADS1115 en voltios (4.096 por defecto).

Sensor BME280 - Temperatura, humedad y presión (opcional)
- BME280: habilita el sensor BME280 (True/False).
- BME280_ADDRESS: dirección I2C del sensor BME280 (p. ej. 0x76).
- BME280_CORRECTION_TEMPERATURE: corrección para temperatura en grados (0 por defecto).
- BME280_CORRECTION_PRESSURE: corrección para presión (0 por defecto).
- BME280_CORRECTION_HUMIDITY: corrección para humedad (0 por defecto).
- BME280_SAMPLE_DELAY_MS: retardo entre muestras en milisegundos (500 por defecto).

Ventilador (opcional)
- FAN: habilita el control del ventilador (True/False).
- FAN_PIN: GPIO que controla el ventilador (p. ej. 3).

Humidificador (opcional)
- HUMIDIFIER: habilita el control del humidificador (True/False).
- HUMIDIFIER_PIN: GPIO que controla el humidificador (p. ej. 8).

General
- DEBUG: activa salida de depuración por consola (True/False).

Nota: Algunas implementaciones pueden usar variables adicionales como DEVICE_ID. 
Si tu backend lo requiere, consúltalo en [docs/api.md](docs/api.md) o en tu implementación de API.

## Ejemplo de plantilla (basado en src/.env.example.py)

# Wireless
HOSTNAME = "SmartPlant"
AP_NAME = ""
AP_PASS = ""

# Puntos de accesos alternativos, para redes de respaldo o si mueves la RPI
ALTERNATIVES_AP = [
    #{"ssid": "", "password": ""},
]

# Datos para la API
API_URL = "http://localhost:8000/api"
API_TOKEN = "apitoken"
API_UPLOAD = True
API_UPLOAD_INTERVAL = 30 # Intervalo entre subidas de datos a la API (En minutos, a partir de 5)

## Batería
BATTERY = False ## Indica si se activa la batería para este dispositivo
BATTERY_PIN = 26
BATTERY_MIN_VOLTAGE = 2.7 ## Mínimo voltaje, batería vacía -> 0%
BATTERY_MAX_VOLTAGE = 4.15 ## Máximo voltaje con batería llena -> 100%

## ADC / Batería (configuración de lectura)
BATTERY_DIVIDER_R1_OHMS = 100000  # Resistencia superior del divisor (desde + batería al pin)
BATTERY_DIVIDER_R2_OHMS = 100000  # Resistencia inferior del divisor (desde pin a GND)
BATTERY_ADC_CALIBRATION_SCALE = 1.0  # Factor de escala para calibración fina
BATTERY_ADC_CALIBRATION_OFFSET = 0.0  # Offset para calibración fina (en voltios)
BATTERY_ESTIMATION_ALPHA = 0.1  # Factor de suavizado EMA para estimar voltaje (0<alpha<=1)

## Iluminación
LIGHT_CONTROL = False ## Indica si se activa una señal de GPIO para iluminación de plantas en interior
LIGHT_CONTROL_PIN = 1 ## Pin que da la señal de iluminación

## Motor de agua para riego
WATERING_MOTOR = False ## Indica si se activa el motor de agua para riego
WATERING_MOTOR_PIN = 0 ## Pin GPIO que activa el motor

## Boya para detectar nivel de agua
WATER_LEVEL_SENSOR = False ## Indica si se activa el sensor de nivel de agua
WATER_LEVEL_SENSOR_PIN = 2 ## Pin GPIO que detecta el nivel de agua

## Control de cantidad de plantas
ADS1115 = False ## Indica si está habilitado. Si no está, se utilizará ADC interno de la RPI
ADS1115_ADDRESS = 0x48 ## Dirección del módulo
ADS1115_QUANTITY = 4 ## Cantidad de plantas que monitoriza
ADS1115_2 = False ## Indica si se habilita un segundo módulo ADC adicional para hasta 8 plantas.
ADS1115_2_ADDRESS = 0x49 ## Dirección del módulo
ADS1115_2_QUANTITY = 4 ## Cantidad de plantas que monitoriza

## Humedad de suelo (calibración y muestreo)
SOIL_DRY_VOLTAGE = 3.5   # Voltaje en seco (V alto)
SOIL_WET_VOLTAGE = 1.8   # Voltaje en húmedo (V bajo)
SOIL_CALIBRATION_SCALE = 1.0  # Escala de calibración
SOIL_CALIBRATION_OFFSET = 0.0 # Offset de calibración (V)
SOIL_SAMPLES = 8              # Número de muestras para promediar
SOIL_SAMPLE_DELAY_MS = 5      # Retardo entre muestras (ms)
SOIL_ADS1115_PGA_FS = 4.096   # Rango a plena escala del ADS (V)

## Sensor BME280
BME280 = True
BME280_ADDRESS = 0x76
BME280_CORRECTION_TEMPERATURE = 0
BME280_CORRECTION_PRESSURE = 0
BME280_CORRECTION_HUMIDITY = 0
BME280_SAMPLE_DELAY_MS = 500

## Ventilador
FAN = False
FAN_PIN = 3

## Humidificador
HUMIDIFIER = False ## Indica si se activa el humidificador
HUMIDIFIER_PIN = 8 ## Pin GPIO que activa el humidificador

# Indica si está en modo debug la aplicación
DEBUG = False

## Pasos de configuración
1. Copia src/.env.example.py a env.py (o crea env.py tomando como base ese fichero).
2. Rellena HOSTNAME, AP_NAME y AP_PASS, y si procede ALTERNATIVES_AP.
3. Configura API_URL, API_TOKEN y ajusta API_UPLOAD/INTERVAL según tu caso.
4. Si usas batería, iluminación, motor de riego o sensor de nivel, habilita los flags y verifica los pines en docs/pinout.md.
5. Ajusta DEBUG según necesidad.

Consulta también [docs/api.md](docs/api.md) para los formatos de petición y respuesta de la API.