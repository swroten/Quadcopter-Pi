# Code for IMU
#!/usr/bin/env python2
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
        # Create failure counter
        self.failure_counter = 0
        self.max_failures = 5
        
        # Print Statement about Connecting to IMU
        print("Connecting to Adafruit IMU...")
        
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
        self.sys, self.gyro, self.accel, self.mag = self.bno.get_calibration_status()

    #Scale Specified Value 
    def scale(self, valueIn, baseMin, baseMax, limitMin, limitMax):
        # return Scaled Value
        return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)))
        
    def update(self):
        try:
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            self.heading, self.roll, self.pitch = self.bno.read_euler()

            # Clear failure counter if successful
            self.failure_counter = 0
        except:
            # Increment Failure Counter
            self.failure_counter = self.failure_counter + 1

            # if greater than max failures, throw exception
            if (self.failure_counter > self.max_failures):
                raise

    def get_raw_roll(self):
        return self.roll

    def get_raw_pitch(self):
        return self.pitch

    def get_raw_yaw(self):
        return self.heading

    def get_scaled_roll(self):
        # Initialize Scaled Roll
        scaled_roll = self.scale(self.roll, -90.0, 90.0, -1.0, 1.0)

        # return a value between -1.0 and 1.0
        return min(1.0, max(-1.0, scaled_roll))

    def get_scaled_pitch(self):
        # Initialize Scaled Pitch
        scaled_pitch = self.scale(self.pitch, -180.0, 180.0, -1.0, 1.0)

        # return a value between -1.0 and 1.0
        return min(1.0, max(-1.0, scaled_pitch))

    def get_scaled_yaw(self):
        # Initialize Scaled Yaw
        scaled_yaw = 0.0

        # if between 0 and 180 degrees
        if ((self.heading > 0.0) and (self.heading <= 180.0)):
            scaled_yaw = self.scale(self.heading, 0.0, 180.0, 0.0, 1.0)
        # otherwise it is between 180 and 360 degrees
        else:
            scaled_yaw = self.scale(self.heading, 180.0, 360.0, -1.0, 0.0)

        # return a value between -1.0 and 1.0
        return min(1.0, max(-1.0, scaled_yaw))
