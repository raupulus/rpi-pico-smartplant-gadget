import time
from machine import Pin, ADC

# Intento importar variables de entorno si existen
try:
    import env as ENV
except Exception:
    ENV = None


class SoilMoisture:

    def __init__(self, rpi, pin=None, dry_voltage=None, wet_voltage=None,
                 calibration_scale=None, calibration_offset=None,
                 samples=None, sample_delay_ms=None):
        self.RPI = rpi
        self.pin = pin
        self.adc = ADC(pin) if pin is not None else None

        # Referencia y factor ADC
        self.vref = getattr(rpi, 'voltage_working', 3.3)
        self.adc_factor = getattr(rpi, 'adc_conversion_factor', self.vref / 65535)

        # Umbrales de humedad (V seco > V húmedo)
        if dry_voltage is None:
            dry_voltage = getattr(ENV, 'SOIL_DRY_VOLTAGE', 3.5)
        if wet_voltage is None:
            wet_voltage = getattr(ENV, 'SOIL_WET_VOLTAGE', 1.8)
        # Garantizar orden correcto
        if wet_voltage > dry_voltage:
            dry_voltage, wet_voltage = wet_voltage, dry_voltage
        self.dry_voltage = float(dry_voltage)
        self.wet_voltage = float(wet_voltage)

        # Calibración fina
        self.cal_scale = calibration_scale if calibration_scale is not None else getattr(ENV, 'SOIL_CALIBRATION_SCALE', 1.0)
        self.cal_offset = calibration_offset if calibration_offset is not None else getattr(ENV, 'SOIL_CALIBRATION_OFFSET', 0.0)

        # Muestreo
        self.samples = samples if samples is not None else getattr(ENV, 'SOIL_SAMPLES', 8)
        self.sample_delay_ms = sample_delay_ms if sample_delay_ms is not None else getattr(ENV, 'SOIL_SAMPLE_DELAY_MS', 5)

        # Estadísticas por fuente
        self.stats = {}

    def _update_stats(self, source, voltage, percent):
        s = self.stats.get(source, {})
        if s.get('voltage_min') is None or (voltage is not None and voltage < s.get('voltage_min', voltage)):
            s['voltage_min'] = voltage
        if s.get('voltage_max') is None or (voltage is not None and voltage > s.get('voltage_max', voltage)):
            s['voltage_max'] = voltage
        if s.get('percent_min') is None or percent < s.get('percent_min', percent):
            s['percent_min'] = percent
        if s.get('percent_max') is None or percent > s.get('percent_max', percent):
            s['percent_max'] = percent
        self.stats[source] = s

    def map_voltage_to_percent(self, voltage):
        # Aplico calibración (scale/offset)
        v_cal = (float(voltage) * float(self.cal_scale)) + float(self.cal_offset)
        dv = self.dry_voltage
        wv = self.wet_voltage
        if dv == wv:
            return 0.0, v_cal
        percent = (dv - v_cal) / (dv - wv) * 100.0
        if percent < 0.0:
            percent = 0.0
        elif percent > 100.0:
            percent = 100.0
        return percent, v_cal

    def read_analog(self, samples=None, sample_delay_ms=None):
        """
        Lee humedad del suelo con el ADC interno de la Pico.
        Retorna voltaje y porcentaje (0% = seco, 100% = húmedo).
        """
        if self.adc is None:
            raise ValueError("No ADC pin configured in SoilMoisture instance")

        n = int(samples if samples is not None else self.samples)
        n = n if n > 0 else 1
        delay = int(sample_delay_ms if sample_delay_ms is not None else self.sample_delay_ms)

        total = 0
        for _ in range(n):
            total += self.adc.read_u16()
            if delay > 0:
                time.sleep_ms(delay)
        raw_avg = total // n
        voltage = raw_avg * self.adc_factor

        percent, v_cal = self.map_voltage_to_percent(voltage)
        self._update_stats('pico_adc', v_cal, percent)

        return {
            #'source': 'pico_adc',
            #'raw': raw_avg,
            'voltage': round(v_cal, 4),
            'humidity_percent': round(percent, 1),
            #'dry_voltage': self.dry_voltage,
            #'wet_voltage': self.wet_voltage,
            #'samples': n,
            #'ts_ms': time.ticks_ms(),
            #'stats': self.stats.get('pico_adc', {}).copy(),
        }

    def read_grow_sensor_frequency(self, pin, measurement_time=1.0):
        """
        Lee un sensor Grow de Pimoroni basado en PFM (Pulse-Frequency Modulation).

        Args:
            pin (int): Número del pin GPIO conectado al sensor
            measurement_time (float): Tiempo de medición en segundos (default: 1.0s)

        Returns:
            dict: Frecuencia medida y porcentaje estimado de humedad
        """
        gpio_pin = Pin(pin, Pin.IN)

        pulse_count = 0
        start_time = time.ticks_ms()
        last_state = gpio_pin.value()

        # Contar pulsos durante el tiempo especificado
        while time.ticks_diff(time.ticks_ms(), start_time) < (measurement_time * 1000):
            current_state = gpio_pin.value()

            # Detectar flanco ascendente
            if current_state == 1 and last_state == 0:
                pulse_count += 1

            last_state = current_state

        # Calcular frecuencia
        frequency = pulse_count / measurement_time

        # Convertir a porcentaje de humedad
        # Rango típico: 2Hz (seco) - 30Hz (húmedo)
        min_freq = 2.0   # Frecuencia en seco
        max_freq = 30.0  # Frecuencia en húmedo

        if frequency <= min_freq:
            humidity_percent = 0.0
        elif frequency >= max_freq:
            humidity_percent = 100.0
        else:
            humidity_percent = ((frequency - min_freq) / (max_freq - min_freq)) * 100.0

        self._update_stats('grow', None, humidity_percent)

        return {
            'source': 'grow',
            'frequency_hz': round(frequency, 2),
            'humidity_percent': round(humidity_percent, 1),
            'pulse_count': pulse_count,
            'measurement_time': measurement_time,
            'ts_ms': time.ticks_ms(),
            'stats': self.stats.get('grow', {}).copy(),
        }

    def read_grow_sensor_interrupt(self, pin, callback_function):
        """
        Configuración alternativa usando interrupciones para mayor precisión.

        Args:
            pin (int): Pin GPIO del sensor
            callback_function: Función a llamar en cada pulso

        Returns:
            Pin configurado con interrupción
        """
        gpio_pin = Pin(pin, Pin.IN)

        # Configurar interrupción en flanco ascendente
        gpio_pin.irq(trigger=Pin.IRQ_RISING, handler=callback_function)

        return gpio_pin

    def calculate_grow_humidity_from_frequency(self, frequency):
        """
        Convierte frecuencia a porcentaje de humedad para sensores Grow.

        Args:
            frequency (float): Frecuencia medida en Hz

        Returns:
            float: Porcentaje de humedad (0-100%)
        """
        # Calibración típica para sensores Grow
        min_freq = 2.0   # Hz en aire seco
        max_freq = 30.0  # Hz en agua

        if frequency <= min_freq:
            return 0.0
        elif frequency >= max_freq:
            return 100.0
        else:
            return ((frequency - min_freq) / (max_freq - min_freq)) * 100.0
