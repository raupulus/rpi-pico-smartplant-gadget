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
API_UPLOAD_INTERVAL = 30 # Intervalo entre subidas de datos a la API (En minutos)

## Batería
BATTERY = False ## Indica si se activa la batería para este dispositivo
BATTERY_PIN = 27
BATTERY_VOLTAGE = 3.7 ## Voltaje por diseño
BATTERY_MIN_VOLTAGE = 2.7 ## Mínimo voltaje, batería vacía -> 0%
BATTERY_MAX_VOLTAGE = 4.2 ## Máximo voltaje con batería llena -> 100%

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

# Indica si está en modo debug la aplicación
DEBUG = False
