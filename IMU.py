# Code for IMU
import gps
import logging
import sys
import time
import os
import serial

# Import Adafruit BNO055
from Adafruit_BNO055 import BNO055

# Define Class for IMU
class IMU:
    def __init__(self):    
        # Print Statement about Connecting to IMU
        print("Connecting to Adafruit IMU...")
    
        # Enable verbose debug logging if -v is passed as a parameter.
        if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
            logging.basicConfig(level=logging.DEBUG)
        
        # Raspberry Pi configuration with serial UART and RST connected to GPIO 18: 
        self.bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
        
        # Initialize the BNO055 and stop if something went wrong.
        if not self.bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

        # Print system status and self test result.
        self.status, self.self_test, self.error = self.bno.get_system_status()
        print('System status: {0}'.format(self.status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self.self_test))
    
        # Print out an error if system status is in error mode.
        if self.status == 0x01:
            print('System error: {0}'.format(self.error))
            print('See datasheet section 4.3.59 for the meaning.')

        # Print BNO055 software revision and other diagnostic data.
        self.sw, self.bl, self.accel, self.mag, self.gyro = self.bno.get_revision()
        print('Software version:   {0}'.format(self.sw))
        print('Bootloader version: {0}'.format(self.bl))
        print('Accelerometer ID:   0x{0:02X}'.format(self.accel))
        print('Magnetometer ID:    0x{0:02X}'.format(self.mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(self.gyro))
        
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        self.heading, self.roll, self.pitch = self.bno.read_euler()        
        
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, self.gyro, self.accel, self.mag = self.bno.get_calibration_status()
        
    def PrintIMUValues(self):
        print("Roll,Pitch,Yaw")
        while True:
            print('{0},{1},{2}'.format(self.roll, self.pitch, self.heading))            
    
    def ReadIMUValues(self):
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        self.heading, self.roll, self.pitch = self.bno.read_euler()