# (c) stonatm@gmail.com
# dht11 dht12 onewire library
from machine import Pin
from esp import dht_readinto

def readHumidity(pin):
  buf = bytearray(5)
  try:
    dht_readinto(Pin(pin), buf)
  except:
    pass
  return (buf[0] + buf[1]*0.1)

def readTemperature(pin):
  buf = bytearray(5)
  try:
    dht_readinto(Pin(pin), buf)
  except:
    pass
  return (buf[2] + buf[3]*0.1)
