# (c) stonatm@gmail.com

# Hc-sr04 ultrasonic distance sensor library
class hcsr04:

  from machine import Pin
  import time

  ECHO = None
  TRIG = None

  def init(echo_pin, trig_pin):
    try:
      hcsr04.ECHO = hcsr04.Pin(echo_pin, hcsr04.Pin.IN)
      hcsr04.TRIG = hcsr04.Pin(trig_pin, hcsr04.Pin.OUT)
    except:
      pass

  def _measure():
    if (not hcsr04.ECHO) or not(hcsr04.TRIG):
      return 0
    #send trigger signal
    hcsr04.TRIG.value(0)
    hcsr04.time.sleep_us(5)
    hcsr04.TRIG.value(1)
    hcsr04.time.sleep_us(10)
    hcsr04.TRIG.value(0)
    #calculate duration of echo signal in microseconds
    while hcsr04.ECHO.value() == 0:
      pulse_start = hcsr04.time.ticks_us()
    while hcsr04.ECHO.value() == 1:
      pulse_end = hcsr04.time.ticks_us()
    pulse_dur = pulse_end - pulse_start
    # calculate distance in cm
    distance = pulse_dur * 17150 / 1000000
    return int(distance)

  def distance_cm():
    return hcsr04._measure()

  def distance_m():
    return hcsr04._measure() / 100

# Sharp GP2Y0A21YK infrared distance sensor
# model: "1080" [10cm to 80cm]
class sharp1080:

  import math

  ADC_RES = None
  ADC_PIN = None

  ESP8266 = 1
  ESP32 = 2
  PICO = 3

  INIT = False
  DEBUG = False
  FAST = False

  def init(pin, model):
    sharp1080.ADC_PIN = pin
    if model == sharp1080.ESP8266:
      sharp1080.ADC_RES = 10
      sharp1080.INIT = sharp1080.ESP8266
    elif model == sharp1080.ESP32:
      sharp1080.ADC_RES = 12
      sharp1080.INIT = sharp1080.ESP32
    elif model == sharp1080.PICO:
      sharp1080.ADC_RES = 16
      sharp1080.INIT = sharp1080.PICO
    else:
      sharp1080.INIT = False

  # read sensor output voltage
  def _read_adc():
    # exit if adc resolution was not set
    if not sharp1080.INIT:
      return 0

    from machine import ADC, Pin
    
    conversion_factor = 3.3 / ((2**sharp1080.ADC_RES)-1)

    # raspberry pico
    if sharp1080.INIT == sharp1080.PICO:
      adc = ADC(Pin(sharp1080.ADC_PIN))
      raw = adc.read_u16()

    # esp8266
    if sharp1080.INIT == sharp1080.ESP8266:
      adc = ADC(0)
      raw = adc.read()

    # esp32
    if sharp1080.INIT == sharp1080.ESP32:
      adc = ADC(Pin(sharp1080.ADC_PIN))
      adc.atten(ADC.ATTN_11DB)
      adc.width(ADC.WIDTH_12BIT)
      raw = adc.read()

    volt = raw * conversion_factor
    if sharp1080.DEBUG: print("adc_read: " + str(volt) + "V")
    return volt

  # return precalculated values
  def _calculate_distance_table(volt):
    if volt >= 2.60: return 10
    if volt >= 2.10: return 12
    if volt >= 1.85: return 14
    if volt >= 1.65: return 15
    if volt >= 1.50: return 18
    if volt >= 1.39: return 20
    if volt >= 1.15: return 25
    if volt >= 0.98: return 30
    if volt >= 0.85: return 35
    if volt >= 0.75: return 40
    if volt >= 0.67: return 45
    if volt >= 0.61: return 50
    if volt >= 0.59: return 55
    if volt >= 0.55: return 60
    if volt >= 0.50: return 65
    if volt >= 0.48: return 70
    if volt >= 0.45: return 75
    if volt >= 0.42: return 80
    if volt >= 0: return 0

  # returns approximate values calculated using the function
  def _calculate_distance_function(volt):
    if volt == 0:
      return 0
    dist = 1.05652 + (27.7189 / sharp1080.math.pow(volt, 1.22042))
    return int(dist)

  # return distance in m
  def distance_m():
    return (sharp1080.distance_cm() / 100)

  # return distance in cm
  def distance_cm():
    if sharp1080.FAST:
      return (sharp1080._calculate_distance_table(sharp1080._read_adc()))
    else:
      return (sharp1080._calculate_distance_function(sharp1080._read_adc()))