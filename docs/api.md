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
    "current_utc": "2025-08-09 15:00",
    "outdoor": false
  },
  "plants": [
    {
      "id": 1,
      "adc": 0,
      "name": "Planta 1",
      "optimal_temperature": 20,
      "optimal_soil_humidity": 20,
      "optimal_air_humidity": 20
    },
    {
      "id": 2,
      "adc": 1,
      "name": "Planta 1",
      "optimal_temperature": 28,
      "optimal_soil_humidity": 46,
      "optimal_air_humidity": 70
    }
  ],
  "system": {
    "has_water_pump": false,
    "has_water_level_sensor": false,
    "has_light_sensor": false,
    "low_power_mode": false,
    "watering_time_interval": 5,
    "fan_time": [
        {
          "start": "09:00",
          "end": "10:00"
        },
        {
          "start": "17:30",
          "end": "18:30"
        }     
      ],
    "prefer_watering_time": [
        {
          "start": "09:00",
          "end": "10:00"
        },
        {
          "start": "17:30",
          "end": "18:30"
        }
      ],
    "light_time": [
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
}
```

location:

- outdoor: Indica si la planta se encuentra fuera de la casa.

system:
- has_water_pump: Indica si tiene motor de riego automático
- has_water_level_sensor: Indica si tiene sensor para nivel de agua, al 
  tenerlo limita encender motor de riego si el nivel es bajo
- low_power_mode: Indica si tiene configurado modo bajo consumo. Esto 
  minimiza tiempos de lecturas en sensores, subidas a la api y los leds 
  parpadean en lugar de encenderse.

TODO: Plantear si esta configuración interesa guardarla en la memoria del 
dispositivo. Esto permite usarse sin internet en el futuro manteniendo la misma
configuración.

TODO: Plantear si añadimos intervalo de riego, es decir, regará en el rango 
de horas con preferencia pero durante el tiempo que indiquemos (por defecto 
5 segundos)



## Enviando datos

Enviando información a la API

## Example Request

```json
{
  "device": {
    "device_id": "rpi_pico_w_e661640843114021",
    "firmware": "1.26.0",
    "hardware": "Raspberry Pi Pico",
    "temperature": 37,
    "battery": 86,
    "battery_voltage": 3.9,
    "uptime": 1234567890,
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "wifi_rssi": -50,
    "wifi_ssid": "SSID",
    "wifi_ip": "192.168.1.100"
  },
  "plants": [
    {
      "id": 1,
      "adc": 0,
      "soil_humidity": 20
    },
    {
      "id": 2,
      "adc": 1,
      "soil_humidity": 20
    }
  ],
  "system": {
    "fan_on": null,
    "light_on": null,
    "water_level_correct": null
  },
  "temperature": 20,
  "humidity": 20,
  "pressure": 20,
  "light": {
    "uv_index": 0,
    "lux": 0,
    "uva": 0,
    "uvb": 0
  }
}
```

Device:

- device_id: Se obtiene del dispositivo, machine.unique_id() en bytes (Se sube 
  ese valor convertido a hexadecimal como string: ubinascii.hexlify
  (unique_id).decode()). Esto permite identificar el dispositivo en la API. 
  Además, se añade delante "rpi_pico_w_" para evitar colisiones entre otros 
  fabricantes como esp32. Así me aseguro identificarlo en la api de forma única.
- battery: Indica el porcentaje de batería actual, si es null se ignora ya 
  que no aplica.

system

- water_level_correct: Indica si hay agua suficiente para riego. Si es null 
  se ignora ya que no aplica.

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
