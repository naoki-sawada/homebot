import wiringpi
import os
import struct
from time import sleep

class Temphudi:
    def __init__(self):
        wiringpi.wiringPiSetup()
        self.i2c = wiringpi.I2C()
        self.dev = self.i2c.setup(0x40)

    def get(self):
        self.i2c.writeReg16(self.dev,0x02,0x10) #Temp + Hidi 32-bit transfer mode, LSB-MSB inverted, why?
        self.i2c.writeReg8(self.dev,0x00,0x00) #start conversion.
        sleep((6350.0 + 6500.0 +  500.0)/1000000.0) #wait for conversion.
        #LSB-MSB inverted, again...
        temp = ((struct.unpack('4B', os.read(self.dev,4)))[0] << 8 | (struct.unpack('4B', os.read(self.dev,4)))[1])
        hudi = ((struct.unpack('4B', os.read(self.dev,4)))[2] << 8 | (struct.unpack('4B', os.read(self.dev,4)))[3])
        temp = round(((temp / 65535.0) * 165 - 40), 1)
        hudi = round(((hudi / 65535.0) * 100), 1)
        return temp, hudi
