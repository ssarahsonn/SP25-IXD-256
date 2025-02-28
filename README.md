# Stage Design

#Final code
import os, sys, io
import M5
from M5 import *
#from hardware import RGB
from hardware import I2C
from hardware import Pin
from unit import IMUProUnit
from time import *

# initialize M5 hardware:
M5.begin()

# configure I2C port on pins 1 and 2:
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

# configure IMU on I2C port:
imu = IMUProUnit(i2c)

while True:
    # update M5 hardware:
    M5.update()
    # read accelerometer values from IMU:
    imu_val = imu.get_accelerometer()
    
    # print all (x, y, z) accelerometer values:
    print(imu_val)
    
    # print the X-axis accelerometer value:
    #print(imu_val[0])  # value at index 0
    
    # print the Y-axis accelerometer value:
    #print('y =', imu_val[1])  # value at index 1
    
    # print the X and Y accelerometer values:
    #print(imu_val[0], imu_val[1])
    
    sleep_ms(100)
