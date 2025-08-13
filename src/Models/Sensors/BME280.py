
import time
from machine import I2C
import struct

# Intento importar variables de entorno si existen
try:
    import env as ENV
except Exception:
    ENV = None

class BME280:
    # BME280 I2C addresses
    BME280_I2CADDR = 0x76

    # BME280 register addresses
    BME280_REGISTER_DIG_T1 = 0x88
    BME280_REGISTER_DIG_T2 = 0x8A
    BME280_REGISTER_DIG_T3 = 0x8C
    BME280_REGISTER_DIG_P1 = 0x8E
    BME280_REGISTER_DIG_P2 = 0x90
    BME280_REGISTER_DIG_P3 = 0x92
    BME280_REGISTER_DIG_P4 = 0x94
    BME280_REGISTER_DIG_P5 = 0x96
    BME280_REGISTER_DIG_P6 = 0x98
    BME280_REGISTER_DIG_P7 = 0x9A
    BME280_REGISTER_DIG_P8 = 0x9C
    BME280_REGISTER_DIG_P9 = 0x9E
    BME280_REGISTER_DIG_H1 = 0xA1
    BME280_REGISTER_DIG_H2 = 0xE1
    BME280_REGISTER_DIG_H3 = 0xE3
    BME280_REGISTER_DIG_H4 = 0xE4
    BME280_REGISTER_DIG_H5 = 0xE5
    BME280_REGISTER_DIG_H6 = 0xE7
    BME280_REGISTER_CHIPID = 0xD0
    BME280_REGISTER_VERSION = 0xD1
    BME280_REGISTER_SOFTRESET = 0xE0
    BME280_REGISTER_CAL26 = 0xE1
    BME280_REGISTER_CONTROLHUMID = 0xF2
    BME280_REGISTER_STATUS = 0xF3
    BME280_REGISTER_CONTROL = 0xF4
    BME280_REGISTER_CONFIG = 0xF5
    BME280_REGISTER_PRESSUREDATA = 0xF7
    BME280_REGISTER_TEMPDATA = 0xFA
    BME280_REGISTER_HUMIDDATA = 0xFD

    def __init__(self, rpi=None):
        """
        Inicializa el sensor BME280
        
        Args:
            rpi: Instancia RpiPico para obtener I2C si no se proporciona
            i2c: Instancia I2C personalizada
            address: Dirección I2C del sensor (por defecto desde ENV)
            i2c_bus: Bus I2C a usar (por defecto desde ENV)
        """
        self.rpi = rpi
        
        # Configuración desde ENV
        self.address = getattr(ENV, 'BME280_ADDRESS', self.BME280_I2CADDR)
        self.correction_temp = getattr(ENV, 'BME280_CORRECTION_TEMPERATURE', 0.0)
        self.correction_pressure = getattr(ENV, 'BME280_CORRECTION_PRESSURE', 0.0)
        self.correction_humidity = getattr(ENV, 'BME280_CORRECTION_HUMIDITY', 0.0)
        self.sample_delay_ms = getattr(ENV, 'BME280_SAMPLE_DELAY_MS', 500)
        
        if rpi is not None:
            self.i2c = rpi.i2c0
        else:
            raise ValueError("Se requiere instancia RPI o I2C para inicializar BME280")
        
        if self.i2c is None:
            raise ValueError("No se pudo configurar I2C para BME280")
        
        # Variables para datos de calibración
        self.dig_t1 = 0
        self.dig_t2 = 0
        self.dig_t3 = 0
        self.dig_p1 = 0
        self.dig_p2 = 0
        self.dig_p3 = 0
        self.dig_p4 = 0
        self.dig_p5 = 0
        self.dig_p6 = 0
        self.dig_p7 = 0
        self.dig_p8 = 0
        self.dig_p9 = 0
        self.dig_h1 = 0
        self.dig_h2 = 0
        self.dig_h3 = 0
        self.dig_h4 = 0
        self.dig_h5 = 0
        self.dig_h6 = 0
        
        # Variable para t_fine (necesaria para cálculos de presión y humedad)
        self.t_fine = 0
        
        # Inicializar sensor
        self._init_sensor()

    def _read_register(self, register, length=1):
        """Lee uno o más registros del sensor"""
        try:
            return self.i2c.readfrom_mem(self.address, register, length)
        except Exception as e:
            raise RuntimeError(f"Error leyendo registro {register}: {e}")

    def _write_register(self, register, value):
        """Escribe un valor a un registro del sensor"""
        try:
            self.i2c.writeto_mem(self.address, register, bytearray([value]))
        except Exception as e:
            raise RuntimeError(f"Error escribiendo registro {register}: {e}")

    def _read_u8(self, register):
        """Lee un byte sin signo del registro especificado"""
        result = self._read_register(register, 1)
        return struct.unpack('<B', result)[0]

    def _read_s8(self, register):
        """Lee un byte con signo del registro especificado"""
        result = self._read_u8(register)
        if result > 127:
            result -= 256
        return result

    def _read_u16_le(self, register):
        """Lee un valor de 16 bits sin signo en little endian"""
        result = self._read_register(register, 2)
        return struct.unpack('<H', result)[0]

    def _read_s16_le(self, register):
        """Lee un valor de 16 bits con signo en little endian"""
        result = self._read_register(register, 2)
        return struct.unpack('<h', result)[0]

    def _read_calibration(self):
        """Lee los datos de calibración del sensor usando lecturas individuales"""
        # Leer coeficientes de temperatura (T1-T3) - mismo para BME280 y BMP280
        self.dig_t1 = self._read_u16_le(self.BME280_REGISTER_DIG_T1)
        self.dig_t2 = self._read_s16_le(self.BME280_REGISTER_DIG_T2)
        self.dig_t3 = self._read_s16_le(self.BME280_REGISTER_DIG_T3)
        
        # Leer coeficientes de presión (P1-P9) - mismo para BME280 y BMP280
        self.dig_p1 = self._read_u16_le(self.BME280_REGISTER_DIG_P1)
        self.dig_p2 = self._read_s16_le(self.BME280_REGISTER_DIG_P2)
        self.dig_p3 = self._read_s16_le(self.BME280_REGISTER_DIG_P3)
        self.dig_p4 = self._read_s16_le(self.BME280_REGISTER_DIG_P4)
        self.dig_p5 = self._read_s16_le(self.BME280_REGISTER_DIG_P5)
        self.dig_p6 = self._read_s16_le(self.BME280_REGISTER_DIG_P6)
        self.dig_p7 = self._read_s16_le(self.BME280_REGISTER_DIG_P7)
        self.dig_p8 = self._read_s16_le(self.BME280_REGISTER_DIG_P8)
        self.dig_p9 = self._read_s16_le(self.BME280_REGISTER_DIG_P9)
        
        if self.is_bmp280:
            # BMP280 no tiene sensores de humedad - usar valores por defecto
            self.dig_h1 = 0
            self.dig_h2 = 0
            self.dig_h3 = 0
            self.dig_h4 = 0
            self.dig_h5 = 0
            self.dig_h6 = 0
        else:
            # BME280 coeficientes de humedad
            self.dig_h1 = self._read_u8(self.BME280_REGISTER_DIG_H1)
            self.dig_h2 = self._read_s16_le(self.BME280_REGISTER_DIG_H2)
            self.dig_h3 = self._read_u8(self.BME280_REGISTER_DIG_H3)
            
            # H4 y H5 tienen manejo especial según el ejemplo de trabajo
            h4 = self._read_s8(self.BME280_REGISTER_DIG_H4)
            h4 = (h4 << 24) >> 20
            self.dig_h4 = h4 | (self._read_u8(self.BME280_REGISTER_DIG_H5) & 0x0F)
            
            h5 = self._read_s8(self.BME280_REGISTER_DIG_H6)
            h5 = (h5 << 24) >> 20
            self.dig_h5 = h5 | (self._read_u8(self.BME280_REGISTER_DIG_H5) >> 4 & 0x0F)
            
            self.dig_h6 = self._read_s8(self.BME280_REGISTER_DIG_H6)

    def _init_sensor(self):
        """Inicializa el sensor BME280/BMP280"""
        # Verificar chip ID
        chip_id = struct.unpack('<B', self._read_register(self.BME280_REGISTER_CHIPID))[0]
        
        # Soportar tanto BME280 (0x60) como BMP280 (0x58)
        valid_chip_ids = [0x60, 0x58]  # BME280, BMP280
        if chip_id not in valid_chip_ids:
            raise RuntimeError(f"Chip ID no soportado: 0x{chip_id:02x}, esperados: 0x60 (BME280) o 0x58 (BMP280)")
        
        # Detectar tipo de sensor
        self.is_bmp280 = (chip_id == 0x58)
        self.sensor_type = "BMP280" if self.is_bmp280 else "BME280"
        
        # Leer calibración
        self._read_calibration()
        
        # Configurar oversampling y modo
        # Humedad: oversampling x1
        self._write_register(self.BME280_REGISTER_CONTROLHUMID, 0x01)
        
        # Temperatura: oversampling x2, Presión: oversampling x16, Modo: normal
        self._write_register(self.BME280_REGISTER_CONTROL, 0xB7)
        
        # Filtro off, standby 0.5ms
        self._write_register(self.BME280_REGISTER_CONFIG, 0x00)
        
        # Esperar estabilización
        time.sleep_ms(100)

    def _read_raw_data(self):
        """Lee los datos raw del sensor"""
        # Leer temperatura, presión y humedad de una vez
        data = self._read_register(self.BME280_REGISTER_PRESSUREDATA, 8)
        
        # Extraer datos raw
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw = (data[6] << 8) | data[7]
        
        return temp_raw, pres_raw, hum_raw

    def _compensate_temperature(self, temp_raw):
        """Compensa la temperatura raw y calcula t_fine"""
        var1 = (temp_raw / 16384.0 - self.dig_t1 / 1024.0) * self.dig_t2
        var2 = ((temp_raw / 131072.0 - self.dig_t1 / 8192.0) * 
                (temp_raw / 131072.0 - self.dig_t1 / 8192.0) * self.dig_t3)
        
        self.t_fine = int(var1 + var2)
        temperature = (var1 + var2) / 5120.0
        
        return temperature

    def _compensate_pressure(self, pres_raw):
        """Compensa la presión raw usando t_fine"""
        var1 = self.t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_p6 / 32768.0
        var2 = var2 + var1 * self.dig_p5 * 2.0
        var2 = (var2 / 4.0) + (self.dig_p4 * 65536.0)
        var1 = (self.dig_p3 * var1 * var1 / 524288.0 + self.dig_p2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_p1
        
        if var1 == 0:
            return 0  # Evitar división por cero
        
        pressure = 1048576.0 - pres_raw
        pressure = (pressure - (var2 / 4096.0)) * 6250.0 / var1
        var1 = self.dig_p9 * pressure * pressure / 2147483648.0
        var2 = pressure * self.dig_p8 / 32768.0
        pressure = pressure + (var1 + var2 + self.dig_p7) / 16.0
        
        return pressure / 100.0  # Convertir a hPa

    def _compensate_humidity(self, hum_raw):
        """Compensa la humedad raw usando t_fine"""
        h = self.t_fine - 76800.0
        h = ((hum_raw - (self.dig_h4 * 64.0 + self.dig_h5 / 16384.0 * h)) *
             (self.dig_h2 / 65536.0 * (1.0 + self.dig_h6 / 67108864.0 * h *
             (1.0 + self.dig_h3 / 67108864.0 * h))))
        h = h * (1.0 - self.dig_h1 * h / 524288.0)
        
        if h > 100.0:
            h = 100.0
        elif h < 0.0:
            h = 0.0
        
        return h

    def get_temperature(self):
        """
        Obtiene la temperatura en grados Celsius
        
        Returns:
            float: Temperatura en °C
        """
        temp_raw, _, _ = self._read_raw_data()
        temperature = self._compensate_temperature(temp_raw)
        
        # Aplicar corrección si está configurada
        if self.correction_temp != 0:
            temperature += self.correction_temp
        
        return round(temperature, 2)

    def get_pressure(self):
        """
        Obtiene la presión en hPa
        
        Returns:
            float: Presión en hPa
        """
        temp_raw, pres_raw, _ = self._read_raw_data()
        # Necesitamos calcular temperatura primero para obtener t_fine
        self._compensate_temperature(temp_raw)
        pressure = self._compensate_pressure(pres_raw)
        
        # Aplicar corrección si está configurada
        if self.correction_pressure != 0:
            pressure += self.correction_pressure
        
        return round(pressure, 2)

    def get_humidity(self):
        """
        Obtiene la humedad relativa en %
        
        Returns:
            float: Humedad relativa en % (BME280) o None (BMP280)
        """
        # BMP280 no tiene sensor de humedad
        if self.is_bmp280:
            return None
            
        temp_raw, _, hum_raw = self._read_raw_data()
        # Necesitamos calcular temperatura primero para obtener t_fine
        self._compensate_temperature(temp_raw)
        humidity = self._compensate_humidity(hum_raw)
        
        # Aplicar corrección si está configurada
        if self.correction_humidity != 0:
            humidity += self.correction_humidity
            # Mantener en rango válido después de corrección
            if humidity > 100.0:
                humidity = 100.0
            elif humidity < 0.0:
                humidity = 0.0
        
        return round(humidity, 2)

    def get_all_data(self):
        """
        Obtiene todos los datos del sensor en un solo diccionario
        
        Returns:
            dict: Diccionario con temperatura, presión y humedad (None para BMP280)
        """
        temp_raw, pres_raw, hum_raw = self._read_raw_data()
        
        # Calcular temperatura primero para obtener t_fine
        temperature = self._compensate_temperature(temp_raw)
        pressure = self._compensate_pressure(pres_raw)
        
        # BMP280 no tiene sensor de humedad
        if self.is_bmp280:
            humidity = None
        else:
            humidity = self._compensate_humidity(hum_raw)
            # Aplicar corrección de humedad si está configurada
            if self.correction_humidity != 0:
                humidity += self.correction_humidity
                # Mantener humedad en rango válido
                if humidity > 100.0:
                    humidity = 100.0
                elif humidity < 0.0:
                    humidity = 0.0
        
        # Aplicar correcciones para temperatura y presión
        if self.correction_temp != 0:
            temperature += self.correction_temp
        if self.correction_pressure != 0:
            pressure += self.correction_pressure
        
        result = {
            'temperature': round(temperature, 2),
            'pressure': round(pressure, 2),
            'sensor_type': self.sensor_type,
            #'timestamp_ms': time.ticks_ms()
        }
        
        # Solo agregar humedad si no es None
        if humidity is not None:
            result['humidity'] = round(humidity, 2)
        else:
            result['humidity'] = None
            
        return result