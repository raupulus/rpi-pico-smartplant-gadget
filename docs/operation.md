# Operación del Sistema

Esta sección describe el comportamiento operativo del dispositivo, los indicadores LED y los ciclos de funcionamiento.

## Indicadores visuales (LEDs)

### LEDs de planta

Configuración individual (1-4 planta, 3 LEDs):
- Verde: condiciones óptimas (humedad de suelo en rango ideal).
- Azul: advertencia (fuera del rango óptimo).
- Rojo: crítico (requiere intervención).

Configuración múltiple (4-8 plantas, 2 LEDs):
- Verde: condiciones óptimas.
- Rojo: requiere atención (advertencia o crítico).
- Alternado Verde/Rojo: advertencia.
- Rojo fijo: crítico.

### LEDs de sistema
- LED Encendido:
  - Encendido fijo: sistema OK.
  - Parpadeo lento: bajo consumo.
  - Apagado: sin alimentación o error crítico.
- LED Comunicación API:
  - Parpadeo rápido: comunicando con API.
  - Encendido breve: datos enviados correctamente.
  - Parpadeo lento: error de comunicación.
  - Apagado: sin actividad de red.

## Estados y secuencias

### Secuencia de inicio
1. LED Encendido se activa (inicialización).
2. LED API parpadea durante la descarga de configuración.
3. LEDs de plantas realizan secuencia de prueba.
4. Pausa de 10 segundos.
5. Entrada en modo de monitorización.

### Ciclo de monitorización
1. Lectura de sensores (LED Encendido parpadea).
2. Procesamiento y actualización de LEDs de plantas.
3. Envío a API (LED API activo).
4. Espera hasta el próximo ciclo.

## Consideraciones de energía
- Uso de patrones de parpadeo y reducción de brillo para bajo consumo.
- Resistencias para leds bajando brillo y consumo.
- Modo hibernación (deepsleep) con indicadores mínimos (configurable).

## Escalabilidad operativa
- 1-4 planta: indicadores más detallados (3 estados).
- 4–8 plantas: indicadores simplificados (2 estados + parpadeo).
- Configuración automática según número de plantas detectadas (Si tiene 2 
  módulos ads1115 se utiliza el sistema simplificado).
