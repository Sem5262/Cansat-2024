from machine import Pin, SPI, I2C, UART
from sdcard import SDCard
from rfm69 import RFM69
from gps import GPS
from ms5611 import MS5611
from bme280 import BME280

class Can:
    def __init__(self):
        # Constants
        self.GPS_UART_ID = 0
        
        self.MS5611_I2C_ID = 0
        self.BMP_I2C_ID = 1
        
        self.RFM69HCW_SPI_ID = 0
        self.SD_SPI_ID = 1
        
        
        self.GPS_TX = 0
        self.GPS_RX = 1
        self.RFM69HCW_SCK = 2
        self.RFM69HCW_MOSI = 3
        self.RFM69HCW_MISO = 4
        self.RFM69HCW_NSS = 5
        self.BMP280_SDA = 6
        self.BMP280_SCL = 7
        self.MS5611_SDA = 8
        self.MS5611_SCL = 9
        self.SD_SCK = 10
        self.SD_MOSI = 11
        self.SD_MISO = 12
        self.SD_CS = 13
        self.BUZZER = 14
        self.RFM69HCW_RST = 15

        # Initialize components
        self.sd = self.initialize_sd()
        self.rfm = self.initialize_rfm69()
        self.gps = self.initialize_gps()
        self.ms5611 = self.initialize_ms5611()
        self.bmp280 = self.initialize_bmp280()

    def initialize_sd(self):
        try:
            sd = SDCard(SPI(1, sck=Pin(self.SD_SCK), mosi=Pin(self.SD_MOSI), miso=Pin(self.SD_MISO)), Pin(self.SD_CS))
            return sd
        except OSError as e:
            if "no SD card" in str(e):
                print("Error: SD-card:", e)
            else:
                print("Unexpected OSError:", e)
            return None

    def initialize_rfm69(self):
        try:
            rfm_spi = SPI(self.RFM69HCW_SPI_ID, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB,
                          mosi=Pin(self.RFM69HCW_MOSI), miso=Pin(self.RFM69HCW_MISO), sck=Pin(self.RFM69HCW_SCK))
            rfm_nss = Pin(self.RFM69HCW_NSS, Pin.OUT, value=True)
            rfm_rst = Pin(self.RFM69HCW_RST, Pin.OUT, value=False)

            rfm = RFM69(spi=rfm_spi, nss=rfm_nss, reset=rfm_rst)
            rfm.frequency_mhz = 433.1
            rfm.bitrate = 250000
            rfm.frequency_deviation = 250000
            rfm.tx_power = 20
            rfm.encryption_key = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"

            return rfm
        except RuntimeError as e:
            print("Error: Radio module isn't wired in correctly:", e)
            return None

    def initialize_gps(self):
        return GPS(UART(self.GPS_UART_ID, baudrate=9600, tx=Pin(self.GPS_TX), rx=Pin(self.GPS_RX)))

    def initialize_ms5611(self):
        ms5611_i2c = I2C(self.MS5611_I2C_ID, sda=Pin(self.MS5611_SDA), scl=Pin(self.MS5611_SCL))
        ms5611 = MS5611(ms5611_i2c)
        ms5611.initialize()
        return ms5611

    def initialize_bmp280(self):
        bmp280_i2c = I2C(self.BMP_I2C_ID, sda=Pin(self.BMP280_SDA), scl=Pin(self.BMP280_SCL))
        bmp280 = BME280(i2c=bmp280_i2c)  # Use BME280 class for BMP280
        return bmp280

can = Can()
