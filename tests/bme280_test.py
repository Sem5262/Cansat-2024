
from machine import I2C, Pin
from bme280_advanced import *
from utime import sleep



sda = Pin(0)
scl = Pin(1)

i2c = I2C(0,sda=sda, scl=scl)

bme280 = BME280(i2c=i2c)

while True:
    print(bme280.values)
    sleep(1)