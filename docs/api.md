# Comunicación con la API

## Recibiendo datos

Recibe la configuración de la API

- Horas de riego por cada planta
- Temperatura óptima del ambiente por cada planta
- Temperatura óptima de la tierra por cada planta


La configuración de la API reescribe las preferencias por defecto de cada 
planta.

Esta configuración se realiza en la app/web y se descarga al iniciar de la api.

Luego se actualiza una vez al día mientras no venga solicitado al subir 
datos en la respuesta de la api.

### Example

```json
{
  "location": {
    "latitude": 40.416775,
    "longitude": -3.703790,
    "altitude": 20,
    "timezone": "Europe/Madrid",
    "city": "Madrid",
    "country": "ES",
    "utc_offset": 3600,
    "sunrise": "07:00",
    "sunset": "19:00",
    "current_utc": "2025-08-09 15:00" 
  },
  "plants": [
    {
      "id": 1,
      "adc": 0,
      "name": "Planta 1",
      "optimal_temperature": 20,
      "optimal_soil_humidity": 20,
      "optimal_air_humidity": 20,
      "prefer_watering_time": [
        {
          "start": "09:00",
          "end": "10:00"
        },
        {
          "start": "17:30",
          "end": "18:30"
        }
      ]
    }
  ],
  "system": {
    "has_water_pump": false,
    "has_water_level_sensor": false
  }
}
```

## Enviando datos

Enviando información a la API

## Example Request

```json
{
  "device": {
    "device_id": 1,
    "firmware": "1.25.0",
    "hardware": "Raspberry Pi Pico",
    "battery": 86,
    "uptime": 1234567890,
    "wifi_rssi": -50,
    "wifi_ssid": "SSID",
    "wifi_ip": "192.168.1.100"
  },
  "plants": [
    {
      "id": 1,
      "adc": 0,
      "temperature": 20,
      "humidity": 20,
      "soil_humidity": 20,
      "pressure": 20,
      "light": 20
    }
  ],
  "system": {
    "water_level_correct": null
  }
}
```

## Example Response

```json
{
    "success": true,
    "message": "Data sent successfully",
    "data": {
        "need_sync_configuration": true,
        "need_reboot": false
    }
}
```

## Wifi

## Conexión a la red Principal

## Configurar wifi con múltiples AP auxiliares (por si falla el principal)

