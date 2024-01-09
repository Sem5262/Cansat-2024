from machine import I2C, Pin
import time

from ms5611 import MS5611

sda = Pin(0)
scl = Pin(1)

i2c = I2C(0,sda=sda, scl=scl)

ms5611 = MS5611(i2c)

ms5611.initialize()

while True:
    
    ms5611.update()

    # Read temperature and pressure
    temperature = ms5611.returnTemperature()
    pressure = ms5611.returnPressure()

    print("Temperature: {:.2f} C, Pressure: {:.2f} hPa".format(temperature, pressure))
    
    time.sleep(1)
