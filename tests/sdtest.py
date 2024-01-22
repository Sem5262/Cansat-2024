import machine
import sdcard
import uos

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0,bits=8, firstbit=machine.SPI.MSB,sck=machine.Pin(10),mosi=machine.Pin(11),miso=machine.Pin(12))
sd = sdcard.SDCard(spi, cs)
uos.mount(sd, '/sd')


print("sd-card:",uos.listdir('/sd'))