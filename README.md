# sensors
Simple micropython libraries for various sensors

## distance.py

Simple library which used for **HC-SR04** ultrasonic distance sensor and **Sharp GP2Y0A21YK** (10-80cm range) infrared distance sensor.
Source file: [distance.py](distance.py)

**WARNING:**
The Sharp infrared distance sensor can return a voltage as high as 2.6V above the maximum allowable input voltage for the AD pin on the ESP8266 (1V). This applies to all separate modules like ESP-12, ESP-07 and similar that do not have a onboard resistor voltage divider at the AD input. In this case a resistor divider with values of 220kohm and 100kohm should be used.
![divider.jpg](divider.jpg)
___
```
class hcsr04
```
___
Initialise pins used by sensor
```
hcsr04.init(echo_pin, trig_pin)
```
parameters:
- **echo_pin** - sensor ECHO pin
- **trig_pin** - sensor TRIGGER pin
___
Read measured distance in centimeters from sensor 
```
hcsr04.distance_cm()
```
parameters: none
___
Read measured distance in meters from sensor 
```
hcsr04.distance_m()
```
parameters: none

___
class sharp1080
___
Initialise sensor pin and reading board type. In case of ESP8266 **pin** number may be any number. It has only one AD input pin 

```
sharp1080.init(pin, model)
```

Parameters:
- **pin** - number of pin connected to sensor.
- **model** - model type of board. Avialable values

**1** or **sharp1080.ESP8266** for esp 8266

**2** or **sharp1080.ESP32** for esp 32

**3** or **sharp1080.PICO** for Raspberry Pi Pico
___
Read measured distance in centimeters from sensor.
```
sharp1080.distance_cm()
```
Parameters: none
___
Read measured distance in meters from sensor.
```
sharp1080.distance_m()
```
Parameters: none
___
### example
```
# INFRARED SENSOR
# import library
from distance import sharp1080 as dist
# esp8266 case init
dist.init(0, dist.ESP8266)
# esp32 case init
dist.init(36, dist.ESP32)
# raspberry pi pico case init
dist.init(26, dist.PICO)
# read measured distance
print(dist.distance_cm())
```
___
```
# ULTRASONIC SENSOR
# import library
from distance import hcsr04 as dist
# init sensor
dist.init(4, 5)
# measure distance
print(dist.distance_m())
```
