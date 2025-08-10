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
- BATTERY_VOLTAGE: voltaje nominal de la batería (p. ej. 3.7).
- BATTERY_MIN_VOLTAGE: voltaje mínimo considerado 0%.
- BATTERY_MAX_VOLTAGE: voltaje máximo considerado 100%.

Iluminación (opcional)
- LIGHT_CONTROL: habilita una salida GPIO para iluminación interior (True/False).
- LIGHT_CONTROL_PIN: GPIO que controla la iluminación (recomendado ver pinout.md).

Riego (opcional)
- WATERING_MOTOR: habilita control del motor/bomba de riego (True/False).
- WATERING_MOTOR_PIN: GPIO que activa el motor de agua.

Nivel de agua (opcional)
- WATER_LEVEL_SENSOR: habilita el sensor/boya de nivel de agua (True/False).
- WATER_LEVEL_SENSOR_PIN: GPIO que lee el estado del nivel de agua.

General
- DEBUG: activa salida de depuración por consola (True/False).

Nota: Algunas implementaciones pueden usar variables adicionales como DEVICE_ID. Si tu backend lo requiere, consúltalo en docs/api.md o en tu implementación de API.

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
API_UPLOAD_INTERVAL = 30  # Intervalo entre subidas de datos a la API (minutos)

## Batería
BATTERY = False            # Activa la monitorización de batería
BATTERY_VOLTAGE = 3.7      # Voltaje nominal
BATTERY_MIN_VOLTAGE = 2.7  # Mínimo (0%)
BATTERY_MAX_VOLTAGE = 4.2  # Máximo (100%)

## Iluminación
LIGHT_CONTROL = False      # Salida GPIO para iluminación interior
LIGHT_CONTROL_PIN = 22     # GPIO sugerido

## Motor de agua para riego
WATERING_MOTOR = False     # Controla el motor/bomba de riego
WATERING_MOTOR_PIN = 21    # GPIO sugerido

## Boya para detectar nivel de agua
WATER_LEVEL_SENSOR = False     # Habilita el sensor de nivel (boya)
WATER_LEVEL_SENSOR_PIN = 20    # GPIO configurable (ver pinout.md para sugerencias)

# Modo depuración
DEBUG = False

## Pasos de configuración
1. Copia src/.env.example.py a env.py (o crea env.py tomando como base ese fichero).
2. Rellena HOSTNAME, AP_NAME y AP_PASS, y si procede ALTERNATIVES_AP.
3. Configura API_URL, API_TOKEN y ajusta API_UPLOAD/INTERVAL según tu caso.
4. Si usas batería, iluminación, motor de riego o sensor de nivel, habilita los flags y verifica los pines en docs/pinout.md.
5. Ajusta DEBUG según necesidad.

Consulta también docs/api.md para los formatos de petición y respuesta de la API.