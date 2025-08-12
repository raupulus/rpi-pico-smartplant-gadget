

class ADS1115:

    sensors = []


    def __init__(self, address):
        self.address = address

    def add_sensor(self):

        # Recibir un identificador

        # Crear una instancia de SoilMoisture

        # Guardarlo dentro de self.sensors

        ## OJO: Tener en cuenta en las variables de entorno la cantidad de sensores

        pass

    def read_sensor(self):
        pass


    def read_all_sensors(self):
        stats = None

        for sensor in self.sensors:
            #sensor.read_analog()
            pass

        return stats


