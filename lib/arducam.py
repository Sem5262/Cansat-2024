from OV2640 import *
from time import sleep_ms

class Arducam:
    def __init__(self, cs=None, spi=None, i2c=None):
        self.i2c = i2c
        self.cs = cs
        self.spi = spi
        
    def spi_read(self, register_address):
        buffer = bytearray([register_address & 0x7F])
        
        self.cs.value(0)
        self.spi.write(buffer)        
        self.spi.write_readinto(buffer, buffer) # or use => buffer = spi.read(1) 
        self.cs.value(1)
        
        return buffer[0]
    
    def spi_write(self, register_address, data):
        
        self.cs.value(0)
        self.spi.write(bytearray([register_address | 0x80, data]))
        self.cs.value(1)
        
        return         
        
    def read_fifo_length(self):
        len1= self.spi_read(0x42)
        len2= self.spi_read(0x43)
        len3= self.spi_read(0x44)
        len3= len3 & 0x7f
        lenght=((len3<<16)|(len2<<8)|(len1))& 0x07fffff
        return lenght
    
    def i2c_write(self, RegID, RegDAT):
        self.i2c.writeto(OV2640_I2C_ADDRESS, bytearray([RegID, RegDAT]))
        return
    
    def i2c_read(self, regID):
        self.i2c.writeto(OV2640_I2C_ADDRESS, bytes([regID]))
        return self.i2c.readfrom(OV2640_I2C_ADDRESS, 1)[0]
    
    def i2c_write_list(self, Reg_ID_DAT_list):
        for data in Reg_ID_DAT_list:
            addr = data[0]
            val = data[1]
            self.i2c_write(addr, val)
        return
     
    def test(self):
        while True:
            self.spi_write(0x00, 0x55)
            res = self.spi_read(0x00)
            if res == 0x55:
                print("spi interface is working")
                break
            else:
                sleep_ms(1000)
                print("spi interface not responding correctly")
            
        while True:
            vid = self.i2c_read(OV2640_CHIPID_HIGH)
            pid = self.i2c_read(OV2640_CHIPID_LOW)

            if (vid != 0x26) and ((pid != 0x41) or (pid != 0x42)):
                print("Can't find OV2640 module!")
                sleep_ms(1000)
            else:
                print("OV2640 detected.")
                break
                
        return True
                
    def OV2640_set_JPEG_size(self,size):
        if size==OV2640_160x120:
            self.i2c_write_list(OV2640_160x120_JPEG)
        elif size==OV2640_176x144:
            self.i2c_write_list(OV2640_176x144_JPEG)
        elif size==OV2640_320x240:
            self.i2c_write_list(OV2640_320x240_JPEG)
        elif size==OV2640_352x288:
            self.i2c_write_list(OV2640_352x288_JPEG)
        elif size==OV2640_640x480:
            self.i2c_write_list(OV2640_640x480_JPEG)
        elif size==OV2640_800x600:
            self.i2c_write_list(OV2640_800x600_JPEG)
        elif size==OV2640_1024x768:
            self.i2c_write_list(OV2640_1024x768_JPEG)
        elif size==OV2640_1280x1024:
            self.i2c_write_list(OV2640_1280x1024_JPEG)
        elif size==OV2640_1600x1200:
            self.i2c_write_list(OV2640_1600x1200_JPEG)
        else:
            self.i2c_write_list(OV2640_320x240_JPEG)

    def OV2640_set_Light_Mode(self,result):
        if result==Auto:
            self.i2c_write(0xff,0x00)
            self.i2c_write(0xc7,0x00)
        elif result==Sunny:
            self.i2c_write(0xff,0x00)
            self.i2c_write(0xc7,0x40)
            self.i2c_write(0xcc,0x5e)
            self.i2c_write(0xcd,0x41)
            self.i2c_write(0xce,0x54)
        elif result==Cloudy:
            self.i2c_write(0xff,0x00)
            self.i2c_write(0xc7,0x40)
            self.i2c_write(0xcc,0x65)
            self.i2c_write(0xcd,0x41)
            self.i2c_write(0xce,0x4f)
        elif result==Office:
            self.i2c_write(0xff,0x00)
            self.i2c_write(0xc7,0x40)
            self.i2c_write(0xcc,0x52)
            self.i2c_write(0xcd,0x41)
            self.i2c_write(0xce,0x66)
        elif result==Home:
            self.i2c_write(0xff,0x00)
            self.i2c_write(0xc7,0x40)
            self.i2c_write(0xcc,0x42)
            self.i2c_write(0xcd,0x3f)
            self.i2c_write(0xce,0x71)
        else:
            self.i2c_write(0xff,0x00)
            self.i2c_write(0xc7,0x00)
            
    def OV2640_set_Color_Saturation(self,Saturation):
        if Saturation== Saturation2:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x02)
            self.i2c_write(0x7c, 0x03)
            self.i2c_write(0x7d, 0x68)
            self.i2c_write(0x7d, 0x68)
        elif Saturation== Saturation1:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x02)
            self.i2c_write(0x7c, 0x03)
            self.i2c_write(0x7d, 0x58)
            self.i2c_write(0x7d, 0x58)
        elif Saturation== Saturation0:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x02)
            self.i2c_write(0x7c, 0x03)
            self.i2c_write(0x7d, 0x48)
            self.i2c_write(0x7d, 0x48)
        elif Saturation== Saturation_1:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x02)
            self.i2c_write(0x7c, 0x03)
            self.i2c_write(0x7d, 0x38)
            self.i2c_write(0x7d, 0x38)
        elif Saturation== Saturation_2:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x02)
            self.i2c_write(0x7c, 0x03)
            self.i2c_write(0x7d, 0x28)
            self.i2c_write(0x7d, 0x28)
            
    def OV2640_set_Brightness(self,Brightness):
        if Brightness== Brightness2:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x09)
            self.i2c_write(0x7d, 0x40)
            self.i2c_write(0x7d, 0x00)
        elif Brightness== Brightness1:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x09)
            self.i2c_write(0x7d, 0x30)
            self.i2c_write(0x7d, 0x00)
        elif Brightness== Brightness0:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x09)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x00)
        elif Brightness== Brightness_1:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x09)
            self.i2c_write(0x7d, 0x10)
            self.i2c_write(0x7d, 0x00)
        elif Brightness== Brightness_2:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x09)
            self.i2c_write(0x7d, 0x00)
            self.i2c_write(0x7d, 0x00)
            
    def OV2640_set_Contrast(self,Contrast):
        if Contrast== Contrast2:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x07)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x28)
            self.i2c_write(0x7d, 0x0c)
            self.i2c_write(0x7d, 0x06)
        elif Contrast== Contrast1:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x07)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x24)
            self.i2c_write(0x7d, 0x16)
            self.i2c_write(0x7d, 0x06) 
        elif Contrast== Contrast0:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x07)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x06) 
        elif Contrast== Contrast_1:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x07)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x2a)
            self.i2c_write(0x7d, 0x06)
        elif Contrast== Contrast_2:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x04)
            self.i2c_write(0x7c, 0x07)
            self.i2c_write(0x7d, 0x20)
            self.i2c_write(0x7d, 0x18)
            self.i2c_write(0x7d, 0x34)
            self.i2c_write(0x7d, 0x06)     
    def OV2640_set_Special_effects(self,Special_effect):
        if Special_effect== Antique:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x18)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x40)
            self.i2c_write(0x7d, 0xa6)
        elif Special_effect== Bluish:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x18)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0xa0)
            self.i2c_write(0x7d, 0x40)
        elif Special_effect== Greenish:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x18)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x40)
            self.i2c_write(0x7d, 0x40)
        elif Special_effect== Reddish:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x18)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x40)
            self.i2c_write(0x7d, 0xc0)
        elif Special_effect== BW:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x18)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x80)
            self.i2c_write(0x7d, 0x80)
        elif Special_effect== Negative:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x40)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x80)
            self.i2c_write(0x7d, 0x80)
        elif Special_effect== BWnegative:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x58)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x80)
            self.i2c_write(0x7d, 0x80)
        elif Special_effect== Normal:
            self.i2c_write(0xff, 0x00)
            self.i2c_write(0x7c, 0x00)
            self.i2c_write(0x7d, 0x00)
            self.i2c_write(0x7c, 0x05)
            self.i2c_write(0x7d, 0x80)
            self.i2c_write(0x7d, 0x80)