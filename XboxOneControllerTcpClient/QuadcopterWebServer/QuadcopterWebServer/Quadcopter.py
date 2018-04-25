# Quadcopter Motors

import logging
import sys
import time
import os
import serial
import math

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

        # Set Min & Max Thrust
        self.MinimumThrust = 0.0
        self.MaximumThrust = (0.000000124736 * self.MaximumRPM * self.MaximumRPM)

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

    # Get Observed Raw Throttle
    def get_raw_throttle(self):
        return compute_resultant_vector()

    # Get Observed Scaled Throttle
    def get_scaled_throttle(self):
        return scale(compute_resultant_vector(), self.MinimumThrust, self.MaximumThrust, self.MinimumSignal, self.MaximumSignal)

    # Compute Resultant Vector for all motors
    def compute_resultant_vector(self):
        # Get RPM for each Motor
        front_left_rpm = scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        front_right_rpm = scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        back_left_rpm = scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        back_right_rpm = scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)

        # Get Thrust for each Motor
        front_left_thrust = compute_motor_thrust(front_left_rpm)
        front_right_thrust = compute_motor_thrust(front_right_rpm)
        back_left_thrust = compute_motor_thrust(back_left_rpm)
        back_right_thrust = compute_motor_thrust(back_right_rpm)

        # Get the resultant vector
        return math.sqrt((front_left_thrust * front_left_thrust) +
                         (front_right_thrust * front_right_thrust) + 
                         (back_left_thrust * back_left_thrust) + 
                         (back_right_thrust * back_right_thrust))

    # Compute Static Thrust of a particular motor
    def compute_motor_thrust(self, rpm):
        return (0.000000124736 * rpm * rpm)

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
        self.FrontLeftScaledPulseWidth = step_motor(front_left_setpoint, self.FrontLeftScaledPulseWidth, self.StepRate)
        self.FrontLeftPulseWidth = scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontLeftMinimumPulseWidth, self.FrontLeftMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftPulseWidth)
        print("Front Left Pulse Width: ", self.FrontLeftScaledPulseWidth)

        # Handle Front Right
        self.FrontRightScaledPulseWidth = step_motor(front_right_setpoint, self.FrontRightPulseWidth)
        self.FrontRightPulseWidth = scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontRightMinimumPulseWidth, self.FrontRightMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.FrontRight, self.FrontRightPulseWidth)
        print("Front Right Pulse Width: ", self.FrontRightScaledPulseWidth)
        
        # Handle Back Left
        self.BackLeftScaledPulseWidth = step_motor(back_left_setpoint, self.BackLeftPulseWidth)
        self.BackLeftPulseWidth = scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackLeftMinimumPulseWidth, self.BackLeftMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.BackLeft, self.BackLeftPulseWidth)
        print("Back Left Pulse Width: ", self.BackLeftScaledPulseWidth)
        
        # Handle Back Right
        self.BackRightScaledPulseWidth = step_motor(back_right_setpoint, self.BackRightPulseWidth)
        self.BackRightPulseWidth = scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackRightMinimumPulseWidth, self.BackRightMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.BackRight, self.BackRightPulseWidth)
        print("Back Right Pulse Width: ", self.BackRightScaledPulseWidth)
    
    # Step Individual Motor
    def step_motor(self, setpoint, current, step): 
        # Create local variable for new current value
        newCurrent = current

        # if within one step...
        if (abs(newCurrent - setpoint) < step):
            # set current to setpoint
            newCurrent = setpoint
        # else if greater than demanded setpoint
        elif (newCurrent > setpoint):
            # decrease current pulse width
            newCurrent -= step
        # otherwise
        else:
            # increase current pulse width
            newCurrent += step

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