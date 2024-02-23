import time
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
        
        self.SEALEVEL_PRESSURE = 101325.0
        
        
        self.BUFFER_SIZE =100
        self.current_filename = "/sd/data.csv"
        
        self.operating_mode = 0
        
        # Initialize components
        self.sd = self.initialize_sd()
        self.rfm = self.initialize_rfm69()
        self.gps = self.initialize_gps()
        self.ms5611 = self.initialize_ms5611()
        self.bmp280 = self.initialize_bmp280()
        self.BUFFER = []
        
        self.init_session_directory()
        
        
    def initialize_sd(self):
        """
        Initializes the Micro SD card.

        Returns:
            SDCard: The Micro SD card object.
        """
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
        """
        Initializes the RFM69HCW Transceiver.

        Returns:
            RFM69: The RFM69HCW Transceiver object.
        """
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
        """
        Initializes the GPS module.

        Returns:
            GPS: The GPS module object.
        """
        return GPS(UART(self.GPS_UART_ID, baudrate=9600, tx=Pin(self.GPS_TX), rx=Pin(self.GPS_RX)))

    def initialize_ms5611(self):
         """
        Initializes the MS5611 sensor.

        Returns:
            MS5611: The MS5611 sensor object.
        """
        ms5611_i2c = I2C(self.MS5611_I2C_ID, sda=Pin(self.MS5611_SDA), scl=Pin(self.MS5611_SCL))
        ms5611 = MS5611(ms5611_i2c)
        return ms5611

    def initialize_bmp280(self):
        """
        Initializes the BMP280 sensor.

        Returns:
            BME280: The BMP280 sensor object.
        """
        bmp280_i2c = I2C(self.BMP_I2C_ID, sda=Pin(self.BMP280_SDA), scl=Pin(self.BMP280_SCL))
        bmp280 = BME280(i2c=bmp280_i2c)  # Use BME280 class for BMP280
        return bmp280
    
    def calculate_altitude(self, pressure):
         """
        Calculates altitude based on the provided pressure.

        Args:
            pressure (float): The pressure value.

        Returns:
            float: Calculated altitude.
        """
        try:
            return 44330 * (1.0 - pow(pressure / self.sealevel, 0.1903))
        except Exception as e:
            print("Error calculating altitude:", e)
            return 0.0
    
    def get_ms5611_data(self):
       """
        Reads and returns compensated data from the MS5611 sensor.

        Returns:
            array: Array containing temperature and pressure.
        """
        try:
            data = self.ms5611.read_compensated_data()
            return array("f", (data[0], data[1] / 100)) # convert to hPa
        
        except Exception as e:
            print("Error reading MS5611 data:", e)
            return None, None

    def get_bmp280_data(self):
        """
        Reads and returns compensated data from the BMP280 sensor.

        Returns:
            array: Array containing temperature and pressure.
        """
        try:
            data = self.bmp280.read_compensated_data()
            return array("f", (data[0], data[1] / 100)) # convert to hPa
        except Exception as e:
            print("Error reading BMP280 data:", e)
            return None, None
        
     def get_gps_data(self):
        """
        Update GPS data.

        Returns:
            array: An array containing updated GPS data.
        """
        gps_data = array("f", [None] * 11)

        try:
            self.gps.update()
            gps_data[0] = self.gps.timestamp_utc
            gps_data[1] = self.gps.latitude
            gps_data[2] = self.gps.longitude
            gps_data[3] = self.gps.fix_quality
            gps_data[4] = self.gps.satellites
            gps_data[5] = self.gps.horizontal_dilution
            gps_data[6] = self.gps.altitude_m
            gps_data[7] = self.gps.height_geoid
            gps_data[8] = self.gps.velocity_knots
            gps_data[9] = self.gps.speed_knots
            gps_data[10] = self.gps.track_angle_deg

        except Exception as e:
            print("Error updating GPS data:", e)

        return gps_data
        
     def init_session_directory(self):
        """
        Initializes the session directory on the SD card.
        """
        if self.sd is not None:
            session_dir = "/sd/session"
            try:
                os.mkdir(session_dir)
                print("Session directory created:", session_dir)
            except OSError:
                print("Session directory already exists.")
    
    def store_data_in_buffer(self, data):
        """
        Stores data in the buffer.

        Args:
            data: Data to be stored in the buffer.
        """
        if len(self.buffer) < self.BUFFER_SIZE:
            self.buffer.append(data)
        else:
            self.save_buffer_to_csv()
            self.buffer = []
            
    def save_buffer_to_csv(self):
        """
        Saves data from the buffer to a CSV file on the SD card.
        """
        if self.sd is not None:
            with open(self.current_file_name, 'a') as f:
                f.write('\n'.join(buffer) + '\n')
                