# Quadcopter Motors

import logging
import sys
import time
import os
import serial

#Launching GPIO library
os.system ("sudo pigpiod")

#Wait 1 Second
time.sleep(1)

#importing GPIO library
import pigpio 

# Define Class for Quadcopter Control
class Quadcopter:

    # Initialize
    def __init__(self):    
        # Assign GPIO to Variable for Reference
        self.front_right_motor_pin = 2 #Front Right Motor - Spins Counter Clock Wise
        self.front_left_motor_pin = 3  #Front Left Motor  - Spins Clock Wise
        self.back_right_motor_pin = 4  #Back Right Motor  - Spins Clock Wise
        self.back_left_motor_pin = 17  #Back Left Motor   - Spins Counter Clock Wise

        # Set ESC Min & Max Values
        self.MinimumPulseWidth = 700  # ESC - Min Value
        self.MaximumPulseWidth = 2000 # ESC - Max Value

        # Set Min & Max Signal
        MinimumSignal = 0
        MaximumSignal = 1000

        # Set Min & Max Achievable RPM
        MinimumRPM = 0
        MaximumRPM = 6300

        # Set the Calibrated Motor PulseWidth Minimum
        FrontRightMinimumPulseWidth = 1230
        FrontLeftMinimumPulseWidth = 1265
        BackRightMinimumPulseWidth = 1325
        BackLeftMinimumPulseWidth = 1250

        # Set the Calibrated Motor PulseWidth Maximum
        FrontRightMaximumPulseWidth = 1680
        FrontLeftMaximumPulseWidth = 1780
        BackRightMaximumPulseWidth = 1751
        BackLeftMaximumPulseWidth = 1719
        
        # Get Variable for Setting Pulses
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(FrontRight, 0) 
        self.pi.set_servo_pulsewidth(FrontLeft, 0) 
        self.pi.set_servo_pulsewidth(BackLeft, 0) 
        self.pi.set_servo_pulsewidth(BackRight, 0)

    #This is the arming procedure of an ESC    
    def arm(): 
        print("Connect the battery and press Enter")
        inp = raw_input()    
        if inp == '':
            pi.set_servo_pulsewidth(FrontLeft, 0)
            pi.set_servo_pulsewidth(FrontRight, 0)
            pi.set_servo_pulsewidth(BackLeft, 0)
            pi.set_servo_pulsewidth(BackRight, 0)
            time.sleep(1)
            pi.set_servo_pulsewidth(FrontLeft, MaximumPulseWidth)
            pi.set_servo_pulsewidth(FrontRight, MaximumPulseWidth)
            pi.set_servo_pulsewidth(BackLeft, MaximumPulseWidth)
            pi.set_servo_pulsewidth(BackRight, MaximumPulseWidth)
            time.sleep(1)
            pi.set_servo_pulsewidth(FrontLeft, MinimumPulseWidth)
            pi.set_servo_pulsewidth(FrontRight, MinimumPulseWidth)
            pi.set_servo_pulsewidth(BackLeft, MinimumPulseWidth)
            pi.set_servo_pulsewidth(BackRight, MinimumPulseWidth)
            time.sleep(1)
            control() 

    #This will stop every action your Pi is performing for ESC of course.        
    def stop(): 
        pi.set_servo_pulsewidth(FrontLeft, 0)
        pi.set_servo_pulsewidth(FrontRight, 0)
        pi.set_servo_pulsewidth(BackLeft, 0)
        pi.set_servo_pulsewidth(BackRight, 0)
        pi.stop()

    #Scale Specified Value 
    def scale(self, valueIn, baseMin, baseMax, limitMin, limitMax):
        # return Scaled Value
        return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)))




    
    # Control Motors with Increase / Decrease Controls         
    def control(): 
        print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
        time.sleep(1)

        # Set Speed to Empirical Minimum
        FrontRightSpeed = FrontRightMinimumPulseWidth
        FrontLeftSpeed = FrontLeftMinimumPulseWidth
        BackRightSpeed = BackRightMinimumPulseWidth
        BackLeftSpeed = BackLeftMinimumPulseWidth
        
        print("Controls: ")
        print("  Arm                  = arm")
        print("  Manual               = manual")
        print("  Stop                 = stop")
        print("  Small Speed Decrease = a")
        print("  Small Speed Increase = d")
        print("  Big Speed Decrease   = q")
        print("  Big Speed Increase   = e")
        while True:
            # Set Speed
            pi.set_servo_pulsewidth(FrontLeft, FrontLeftSpeed)
            pi.set_servo_pulsewidth(FrontRight, FrontRightSpeed)
            pi.set_servo_pulsewidth(BackLeft, BackLeftSpeed)
            pi.set_servo_pulsewidth(BackRight, BackRightSpeed)
            
            # Print Current Speed of Each Motor
            print("Front Left Speed = %d" % FrontLeftSpeed)
            print("Front Right Speed = %d" % FrontRightSpeed)
            print("Back Left Speed = %d" % BackLeftSpeed)
            print("Back Right Speed = %d" % BackRightSpeed)

            # Get Input
            inp = raw_input()

            # Perform Requested Function
            if inp == "q":
                # Big Speed Decrement
                FrontLeftSpeed -= 100
                FrontRightSpeed -= 100
                BackLeftSpeed -= 100
                BackRightSpeed -= 100
                
            elif inp == "e":
                # Big Speed Increment
                FrontLeftSpeed += 100
                FrontRightSpeed += 100
                BackLeftSpeed += 100
                BackRightSpeed += 100
                
            elif inp == "d":
                # Small Speed Increment
                FrontLeftSpeed += 10
                FrontRightSpeed += 10
                BackLeftSpeed += 10
                BackRightSpeed += 10
                
            elif inp == "a":
                # Small Speed Decrement
                FrontLeftSpeed -= 10
                FrontRightSpeed -= 10
                BackLeftSpeed -= 10
                BackRightSpeed -= 10

            elif inp == "min":
                # Set all Motors to Min Value
                FrontLeftSpeed = FrontLeftMinimumPulseWidth
                FrontRightSpeed = FrontRightMinimumPulseWidth
                BackLeftSpeed = BackLeftMinimumPulseWidth
                BackRightSpeed = BackRightMinimumPulseWidth
                
            elif inp == "max":
                # Set all Motors to Max Value
                FrontLeftSpeed = FrontLeftMaximumPulseWidth
                FrontRightSpeed = FrontRightMaximumPulseWidth
                BackLeftSpeed = BackLeftMaximumPulseWidth
                BackRightSpeed = BackRightMaximumPulseWidth
                
            elif inp == "stop":
                #going for the stop function
                stop()          
                break
            
            elif inp == "manual":
                #going for the manual function
                manual_drive()
                break
            
            elif inp == "arm":
                #going for the arm function
                arm()
                break
            
            else:
                print("Invalid Control Specified, please try again.")

        
        
        