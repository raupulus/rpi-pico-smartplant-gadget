


class Plant:

    id = None

    # Nombre de la planta.
    name = "Plant"

    # Temperatura ambiente óptima.
    optimal_temperature = 21

    ## Humedad en tierra óptima (100%)
    optimal_soil_humidity = 60

    ## Humedad del aire óptima.
    optimal_air_humidity = 60

    # Rangos de preferencia en los que se puede regar la planta.
    prefer_watering_time = [
        {
            "start": "09:00",
            "end": "10:00"
        },
        {
            "start": "17:30",
            "end": "18:30"
        }
    ]


    def __init__(self, microcntroller, adc):
        self.microcntroller = microcntroller
        self.ADC = adc

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_optimal_temperature(self, temperature):
        self.optimal_temperature = temperature

    def set_optimal_soil_humidity(self, humidity):
        self.optimal_soil_humidity = humidity

    def set_optimal_air_humidity(self, humidity):
        self.optimal_air_humidity = humidity

    def set_prefer_watering_time(self, prefer_watering_time):
        self.prefer_watering_time = prefer_watering_time


