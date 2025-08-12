import gc
from time import sleep_ms
from Models.Api import Api
from Models.RpiPico import RpiPico
#from Models.Sensors.BME280 import BME280
from Models.Sensors.SoilMoisture import SoilMoisture
from Models.System import System
from functions import log

# Importo variables de entorno
import env

# Habilito recolector de basura
gc.enable()

DEBUG = env.DEBUG

# Rpi Pico Model Instance
rpi = RpiPico(ssid=env.AP_NAME, password=env.AP_PASS, debug=DEBUG,
                     alternatives_ap=env.ALTERNATIVES_AP, hostname=env.HOSTNAME)

sleep_ms(100)

# Debug para mostrar el estado del wifi
rpi.wifi_debug()

sleep_ms(100)

# Ejemplo instanciando I2C en bus 0.
# i2c0 = rpi.set_i2c(20, 21, 0, 400000)
# address = 0x03 # Dirección de un dispositivo i2c
# Ya podemos usar nuestro sensor con la dirección almacenada en "address"

# Ejemplo escaneando todos los dispositivos encontrados por I2C.
# print('Dispositivos encontrados por I2C:', i2c0.scan())

# Ejemplo asociando un callback al recibir +3.3v en el gpio 2
# rpi.set_callback_to_pin(2, "LOW", tu_callback)
# rpi.set_callback_to_pin(2, lambda p: print("Se ejecuta el callback"), "LOW")

# Configurando batería externa
if env.BATTERY:
    rpi.set_external_battery(26)
    sleep_ms(200)

# Preparo la instancia para la comunicación con la API
# api = Api(controller=rpi, url=env.API_URL, path=env.API_PATH, token=env.API_TOKEN, device_id=env.DEVICE_ID, debug=env.DEBUG)


# Ejemplo sincronizando reloj RTC
# TODO: Esto solo se hace si hay wifi
# TODO: Antes de sincronizar el RTC, se debe obtener la hora de la API o la
#  zona horaria local que vendrá de la configuración de la api.
"""
sleep_ms(1000)

while not rpi.sync_rtc_time():

    if env.DEBUG:
        print('Intentando Obtener hora RTC de la API')

    sleep_ms(30000)

# Pausa preventiva al desarrollar (ajustar, pero si usas dos hilos puede ahorrar tiempo por bloqueos de hardware ante errores)
sleep_ms(3000)
"""


## Entidad para el sistema
system = System(rpi)



def thread1 ():
    """
    Segundo hilo.

    En este hilo colocamos otras operaciones con cuidado frente a la
    concurrencia.

    Recomiendo utilizar sistemas de bloqueo y pruebas independientes con las
    funcionalidades que vayas a usar en paralelo. Se puede romper la ejecución.
    """

    if env.DEBUG:
        print('')
        print('Inicia hilo principal (thread1)')


soil = SoilMoisture(rpi, pin=27)


def thread0 ():
    """
    Primer hilo, flujo principal de la aplicación.
    En este hilo colocamos toda la lógica principal de funcionamiento.
    """

    log('')
    log("Inicia hilo principal (thread0)")

    log("Sistema: ", system.get_info())

    log(f"ID único del chip rpi pico: {rpi.get_id()}")
    log("Temperatura raspberry pi pico:", str(rpi.get_cpu_temperature()))

    if env.DEBUG:
        log("Batería externa:", rpi.get_battery_stats())

    print("=== Prueba del sensor de humedad ===")

    # Usando la nueva clase SoilMoisture con el ADC interno en el pin 27
    for _ in range(12):
        log("Soil Moisture (analog):", soil.read_analog())
        sleep_ms(100)

    if env.BME280:
        print("=== Prueba del sensor BME280 ===")
        try:
            # Inicializar el sensor BME280
            bme = BME280(rpi=rpi)
            log("BME280 inicializado correctamente")
            sleep_ms(env.BME280_SAMPLE_DELAY_MS)

            # Leer todos los datos de una vez
            all_data = bme.get_all_data()
            log("Datos completos BME280:", all_data)
            sleep_ms(200)

            # Leer datos individuales
            temperature = bme.get_temperature()
            humidity = bme.get_humidity()
            pressure = bme.get_pressure()

            log(f"Temperatura: {temperature}°C")
            log(f"Humedad: {humidity}%")
            log(f"Presión: {pressure} hPa")

        except Exception as e:
            log(f"Error con sensor BME280: {e}")

    # Probando módulos adc ADS1115
    if (env.ADS1115):
        soil_stats = None
        pass

    if (env.ADS1115_2):
        soil_stats2 = None
        pass

    rpi.on(16)
    sleep_ms(1000)
    rpi.off(16)
    rpi.on(17)
    sleep_ms(1000)
    rpi.off(17)
    rpi.on(18)
    sleep_ms(1000)
    rpi.off(18)
    rpi.on(19)
    rpi.on(20)
    rpi.on(21)

    sleep_ms(1000)
    rpi.off(19)
    rpi.off(20)
    rpi.off(21)

    # Resistencias led RGB
    # Rojo y azul 680R
    # Verde 20k

    print("")
    print("Termina ciclo del hilo 0")
    print("")


while True:
    try:
        thread0()
    except Exception as e:
        if env.DEBUG:
            print('Error: ', e)
    finally:
        if env.DEBUG:
            print('Memoria antes de liberar: ', gc.mem_free())

        gc.collect()

        if env.DEBUG:
            print("Memoria después de liberar:", gc.mem_free())

        sleep_ms(2000)
