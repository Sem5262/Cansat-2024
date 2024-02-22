from machine import I2C, Pin
from bme280 import BME280 

# Define I2C pins
i2c = I2C(sda=Pin(6), scl=Pin(7))

bme = BME280(i2c=i2c)


temperature, pressure, altitude = bme.read_compensated_data()

print("Temperature: {:.15f}°C".format(temperature))
print("Pressure: {:.15f}hPa".format(pressure / 100))
print("Altitude: {:.15f} meters".format(altitude))