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
LIGHT_CONTROL_PIN = 22 ## Pin que da la señal de iluminación

## Motor de agua para riego
WATERING_MOTOR = False ## Indica si se activa el motor de agua para riego
WATERING_MOTOR_PIN = 21 ## Pin GPIO que activa el motor

## Boya para detectar nivel de agua
WATER_LEVEL_SENSOR = False ## Indica si se activa el sensor de nivel de agua
WATER_LEVEL_SENSOR_PIN = 23 ## Pin GPIO que detecta el nivel de agua

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
BME280 = False
BME280_ADDRESS = 0x76
BME280_I2C_BUS = 1
BME280_CORRECTION_TEMPERATURE = 2
BME280_CORRECTION_PRESSURE = 1024
BME280_CORRECTION_HUMIDITY = 100
BME280_SAMPLE_DELAY_MS = 500

## Ventilador
FAN = False
FAN_PIN = 99


# Indica si está en modo debug la aplicación
DEBUG = False
