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
        self.FrontRight = 2 #Front Right Motor - Spins Counter Clock Wise
        self.FrontLeft = 3  #Front Left Motor  - Spins Clock Wise
        self.BackRight = 4  #Back Right Motor  - Spins Clock Wise
        self.BackLeft = 17  #Back Left Motor   - Spins Counter Clock Wise

        # Set ESC Min & Max Values
        self.MinimumPulseWidth = 700  # ESC - Min Value
        self.MaximumPulseWidth = 2000 # ESC - Max Value

        # Set Min & Max Signal
        self.MinimumSignal = 0
        self.MaximumSignal = 1000

        # Set Min & Max Achievable RPM
        self.MinimumRPM = 0
        self.MaximumRPM = 6300

        # Set the Calibrated Motor PulseWidth Minimum
        self.FrontRightMinimumPulseWidth = 1230
        self.FrontLeftMinimumPulseWidth = 1265
        self.BackRightMinimumPulseWidth = 1325
        self.BackLeftMinimumPulseWidth = 1250

        # Set the Calibrated Motor PulseWidth Maximum
        self.FrontRightMaximumPulseWidth = 1680
        self.FrontLeftMaximumPulseWidth = 1780
        self.BackRightMaximumPulseWidth = 1751
        self.BackLeftMaximumPulseWidth = 1719
        
        # Get Variable for Setting Pulses
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(self.FrontRight, 0) 
        self.pi.set_servo_pulsewidth(self.FrontLeft, 0) 
        self.pi.set_servo_pulsewidth(self.BackRight, 0)
        self.pi.set_servo_pulsewidth(self.BackLeft, 0) 

        # Create Current Variables for Pulse Width
        self.StepRate = 50
        self.FrontRightPulseWidth = 0
        self.FrontLeftPulseWidth = 0
        self.BackRightPulseWidth = 0
        self.BackLeftPulseWidth = 0
        
        # Create Current Variables for Scaled Pulse Width
        self.FrontRightScaledPulseWidth = 0
        self.FrontLeftScaledPulseWidth = 0
        self.BackRightScaledPulseWidth = 0
        self.BackLeftScaledPulseWidth = 0

    #This will stop every action your Pi is performing for ESC of course.        
    def stop(self): 
        pi.set_servo_pulsewidth(self.FrontRight, 0)
        pi.set_servo_pulsewidth(self.FrontLeft, 0)
        pi.set_servo_pulsewidth(self.BackLeft, 0)
        pi.set_servo_pulsewidth(self.BackRight, 0)
        pi.stop()

    #Scale Specified Value 
    def scale(self, valueIn, baseMin, baseMax, limitMin, limitMax):
        # return Scaled Value
        return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)))

    # Step Motors 
    def step_motors(self, front_left_setpoint, front_right_setpoint, back_left_setpoint, back_right_setpoint):
        # Handle Front Left
        self.FrontLeftScaledPulseWidth = step_motor(front_left_setpoint, self.FrontLeftScaledPulseWidth)
        self.FrontLeftPulseWidth = scale(self.FrontLeftScaledPulseWidth, 
                                         self.MinimumSignal, 
                                         self.MaximumSignal, 
                                         self.FrontLeftMinimumPulseWidth,
                                         self.FrontLeftMaximumPulseWidth)
        pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftPulseWidth)

        # Handle Front Right
        step_motor(front_right_setpoint, self.FrontRightPulseWidth)
        
        # Handle Back Left
        step_motor(back_left_setpoint, self.BackLeftPulseWidth)
        
        # Handle Back Right
        step_motor(back_right_setpoint, self.BackRightPulseWidth)
    
    # Step Individual Motor
    def step_motor(self, setpoint, current): 
        # Create local variable for new current value
        newCurrent = current

        # if within one step...
        if (abs(newCurrent - front_left_setpoint) < self.StepRate):
            # set current to setpoint
            newCurrent = front_left_setpoint
        # else if greater than demanded setpoint
        elif (newCurrent > front_left_setpoint):
            # decrease current pulse width
            newCurrent -= self.StepRate
        # otherwise
        else:
            # increase current pulse width
            newCurrent += self.StepRate

        # return newly calculated
        return newCurrent

    # Arming Procedure for all ESC    
    def arm(self): 
        # Set to 0
        pi.set_servo_pulsewidth(self.FrontLeft, 0) 
        pi.set_servo_pulsewidth(self.FrontRight, 0) 
        pi.set_servo_pulsewidth(self.BackLeft, 0) 
        pi.set_servo_pulsewidth(self.BackRight, 0) 

        # Wait 1 Second
        time.sleep(1) 

        # Set to Maximum Pulse Width
        pi.set_servo_pulsewidth(self.FrontLeft, MaximumPulseWidth) 
        pi.set_servo_pulsewidth(self.FrontRight, MaximumPulseWidth) 
        pi.set_servo_pulsewidth(self.BackLeft, MaximumPulseWidth) 
        pi.set_servo_pulsewidth(self.BackRight, MaximumPulseWidth) 
        
        # Wait 1 Second
        time.sleep(1) 
        
        # Set to Minimum Pulse Width
        pi.set_servo_pulsewidth(self.FrontLeft, MinimumPulseWidth) 
        pi.set_servo_pulsewidth(self.FrontRight, MinimumPulseWidth) 
        pi.set_servo_pulsewidth(self.BackLeft, MinimumPulseWidth) 
        pi.set_servo_pulsewidth(self.BackRight, MinimumPulseWidth) 
        
        # Wait 1 Second
        time.sleep(1)