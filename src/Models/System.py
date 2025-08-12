
import env



class System:
    """
    TODO: Cada día debe volver a sincronizar datos con el servidor.
    """

    fan = {
        "available": env.FAN,
        "active": False,
        "pin": env.FAN_PIN
    }
    light_control = {
        "available": env.LIGHT_CONTROL,
        "active": False,
        "pin": env.LIGHT_CONTROL_PIN
    }
    water_motor = {
        "available": False,
        "active": False,
        "pin": env.WATERING_MOTOR_PIN
    }
    water_level = {
        "available": False,
        "active": False,
        "pin": env.WATER_LEVEL_SENSOR_PIN
    }

    # Mediciones fijas
    weather_sensor = None
    light_senor = None

    weather = {
        "temperature": None,
        "humidity": None,
        "pressure": None
    }

    light = {
        "lux": None,
        "uv_index": None,
        "uva": None,
        "uvb": None
    }

    # Estados
    need_api_sync = False

    def __init__(self, controller, weather_sensor = None, light_sensor = None):
        ## Microcontrolador
        self.controller = controller

        ## Sensor climatológico (Por defecto BME280)
        self.weather_sensor = weather_sensor

        ## Sensor de luz (Puede ser VEML6075 o VEML7000)
        self.light_sensor = light_sensor

    def need_watering(self):
        """
        Comprueba si hay agua para regar, si está en horario para regar,
        si la temperatura es correcta para el riego y si es necesario regar
        :return:
        """

        ## TODO: Plantear como obtener información de las humedad en tierra
        # para las plantas y evitar regar si la humedad es muy alta.

        pass

    def need_light_on(self):
        pass

    def need_light_off(self):
        pass

    def need_fan_on(self):
        pass

    def need_fan_off(self):
        pass

    def active_water_motor(self):
        pass

    def active_light_control(self):
        pass

    def active_fan(self):
        pass

    def check_all_needs(self):
        """
        Comprueba todos los requerimientos para que el planta se encuentre en un estado ideal.
        Marca los estados como True o False de los atributos de la clase.
        fan, light_control, water_motor, water_level
        :return:
        """
        pass


    def read_sensors(self):

        # self.weather_sensor.stats()
        # if self.light_sensor -> self.light_sensor.stats()
        pass

    def get_info(self):
        """
        Actualiza toda la información y estados para devolverlo.
        :return:
        """
        self.check_all_needs()
        self.read_sensors()

        return  {
            "device": self.controller.get_device_info(),
            "fan_on": self.fan.get('active'),
            "light_on": self.light_control.get('active'),
            "water_motor_on": self.water_motor.get('active'),
            "water_level_correct": self.water_level.get('active'),
            "weather": self.weather,
            "light": self.light,
            "need_api_sync": self.need_api_sync
        }