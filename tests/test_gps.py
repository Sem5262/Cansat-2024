from machine import UART, Pin
from gps import GPS
import time
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))  # Replace with your UART configuration
gps = GPS(uart)

while True:
    time.sleep(1)
    if gps.update():
        # New data is available, you can access GPS information through the GPS object.
        print("Latitude:", gps.latitude)
        print("Longitude:", gps.longitude)
        print("Altitude:", gps.altitude_m)
        print("Speed (knots):", gps.speed_knots)
        print("Fix Quality:", gps.fix_quality)
        print("Satellites:", gps.satellites)
