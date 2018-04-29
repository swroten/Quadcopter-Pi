# Quadcopter Motors
#!/usr/bin/env python2
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
        # Set as disarmed
        self.armed = False
        
        # Scaling Limits
        self.OutputMinimum = -1
        self.OutputMaximum = 1
        
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
        self.MaximumThrust = 4 * (0.000000124736 * self.MaximumRPM * self.MaximumRPM)

        # Set Thrust Deadband to 5% of Maximum Thrust
        self.DEADBAND = 0.05 * (self.MaximumThrust - self.MinimumThrust)
 
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
        self.StepRate = 0.05
        self.FrontRightPulseWidth = 0
        self.FrontLeftPulseWidth = 0
        self.BackRightPulseWidth = 0
        self.BackLeftPulseWidth = 0
        
        # Create Current Variables for Scaled Pulse Width
        self.FrontRightScaledPulseWidth = 0
        self.FrontLeftScaledPulseWidth = 0
        self.BackRightScaledPulseWidth = 0
        self.BackLeftScaledPulseWidth = 0

        # Recall Last Throttle
        self.last_raw_throttle = 0.0

        # Create Variables for RPM
        self.FrontRightRPM = 0
        self.FrontLeftRPM = 0
        self.BackRightRPM = 0
        self.BackLeftRPM = 0

        # Observed Thrust
        self.ObservedThrust = 0.0
        self.dThrottle = 0.0

        # Keep Track of Commanded Throttle
        self.DeltaCommand = 0
        self.CommandedThrottle = 0
        self.CommandedThrottleLastPass = 0

    # Get Whether Armed
    def get_is_armed(self):
        return self.armed
        
    # Scale Specified Value 
    def scale(self, valueIn, baseMin, baseMax, limitMin, limitMax):
        # return Scaled Value
        return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)))

    # Compute Static Thrust of a particular motor
    def compute_motor_thrust(self, rpm):
        return (0.000000124736 * rpm * rpm)
    
    # Compute Resultant Vector for all motors
    def compute_resultant_vector(self):
        # Get RPM for each Motor
        self.FrontLeftRPM = self.scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        self.FrontRightRPM = self.scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        self.BackLeftRPM = self.scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        self.BackRightRPM = self.scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)

        # Get Thrust for each Motor
        front_left_thrust = self.compute_motor_thrust(self.FrontLeftRPM)
        front_right_thrust = self.compute_motor_thrust(self.FrontRightRPM)
        back_left_thrust = self.compute_motor_thrust(self.BackLeftRPM)
        back_right_thrust = self.compute_motor_thrust(self.BackRightRPM)

        # Get the resultant vector
        self.ObservedThrust = (front_left_thrust +
                               front_right_thrust + 
                               back_left_thrust + 
                               back_right_thrust)

        # Return
        return self.ObservedThrust


    # Get Observed Raw Throttle
    def get_raw_thrust(self):
        return self.compute_resultant_vector()

    # Get Observed Scaled Throttle
    def get_scaled_thrust(self):
        return self.scale(self.get_raw_thrust(), self.MinimumThrust, self.MaximumThrust, 0.0, self.OutputMaximum)

    #This will stop every action your Pi is performing for ESC of course.        
    def stop(self): 
        self.pi.set_servo_pulsewidth(self.FrontRight, 0)
        self.pi.set_servo_pulsewidth(self.FrontLeft, 0)
        self.pi.set_servo_pulsewidth(self.BackLeft, 0)
        self.pi.set_servo_pulsewidth(self.BackRight, 0)
        self.pi.stop()
        self.armed = False

    # Process Commanded States versus Observed States to Step Motors
    def process_flight_states(self, throttleOutput, rollOutput, pitchOutput, yawOutput):

        # Convert Observed Thrust into Observed Throttle
        #oThrottle = self.get_scaled_thrust()
        #scaledThrottle = abs(cThrottle)

        # Get Error
        #error = abs(scaledThrottle - oThrottle)

        # Step based on Error
        #if (scaledThrottle < oThrottle):
        #    self.dThrottle -= (self.StepRate * error)
        #elif (scaledThrottle > oThrottle):
        #    self.dThrottle += (self.StepRate * error)

        # Make sure command doesn't go below minimum or above maximum
        #if (self.dThrottle < 0):
        #    self.dThrottle = 0
        #elif (self.dThrottle > self.OutputMaximum):
        #    self.dThrottle = self.OutputMaximum
                    
        #print("Throttle -> C: {0:0.2F}, O: {1:0.2F}, D: {2:0.2F}".format(scaledThrottle, oThrottle, self.dThrottle))

        # Get Demanded Output
        #frontLeftDemandedOutput =  self.scale(self.dThrottle, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        #frontRightDemandedOutput =  self.scale(self.dThrottle, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        #backLeftDemandedOutput =  self.scale(self.dThrottle, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        #backRightDemandedOutput =  self.scale(self.dThrottle, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)

        # Get Demanded Output
        frontLeftDemandedOutput = self.scale((throttleOutput + rollOutput - pitchOutput - yawOutput), 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        frontRightDemandedOutput = self.scale((throttleOutput - rollOutput - pitchOutput + yawOutput), 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        backLeftDemandedOutput = self.scale((throttleOutput + rollOutput + pitchOutput + yawOutput), 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        backRightDemandedOutput = self.scale((throttleOutput - rollOutput + pitchOutput - yawOutput), 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        
        # Handle Front Left
        self.FrontLeftScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, frontLeftDemandedOutput))
        self.FrontLeftPulseWidth = self.scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontLeftMinimumPulseWidth, self.FrontLeftMaximumPulseWidth)
        self.pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftPulseWidth)

        # Handle Front Right
        self.FrontRightScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, frontRightDemandedOutput))
        self.FrontRightPulseWidth = self.scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontRightMinimumPulseWidth, self.FrontRightMaximumPulseWidth)
        self.pi.set_servo_pulsewidth(self.FrontRight, self.FrontRightPulseWidth)
        
        # Handle Back Left
        self.BackLeftScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, backLeftDemandedOutput))
        self.BackLeftPulseWidth = self.scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackLeftMinimumPulseWidth, self.BackLeftMaximumPulseWidth)
        self.pi.set_servo_pulsewidth(self.BackLeft, self.BackLeftPulseWidth)
        
        # Handle Back Right
        self.BackRightScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, backRightDemandedOutput))
        self.BackRightPulseWidth = self.scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackRightMinimumPulseWidth, self.BackRightMaximumPulseWidth)
        self.pi.set_servo_pulsewidth(self.BackRight, self.BackRightPulseWidth)

        print("RPM -> FL: {0:0.2F}, FR: {1:0.2F}, BL: {2:0.2F}, BR: {3:0.2F}".format(
        self.FrontLeftRPM,
        self.FrontRightRPM,
        self.BackLeftRPM,
        self.BackRightRPM))        

                    
        #print("Throttle -> C: {0:0.2F}, O: {1:0.2F}, D: {2:0.2F}".format(cThrottle, oThrottle, self.dThrottle))

        #print("T: {0}, R: {1}, P: {2}, Y: {3}".format(dThrottle, rollOutput, pitchOutput, yawOutput))
        
        
        # Print Pulse Width
        #print("Demanded Output -> FL: {0:0.2F}, FR: {1:0.2F}, BL: {2:0.2F}, BR: {3:0.2F}".format(
        #frontLeftDemandedOutput,
        #frontRightDemandedOutput,
        #backLeftDemandedOutput,
        #backRightDemandedOutput))

        # Print Pulse Width
        #print("Pulse Width     -> FL: {0:0.2F}, FR: {1:0.2F}, BL: {2:0.2F}, BR: {3:0.2F}".format(
        #self.FrontLeftScaledPulseWidth,
        #self.FrontRightScaledPulseWidth,
        #self.BackLeftScaledPulseWidth,
        #self.BackRightScaledPulseWidth))
        
    # Arming Procedure for all ESC    
    def arm(self): 
        # Set to 0
        self.pi.set_servo_pulsewidth(self.FrontLeft, 0) 
        self.pi.set_servo_pulsewidth(self.FrontRight, 0) 
        self.pi.set_servo_pulsewidth(self.BackLeft, 0) 
        self.pi.set_servo_pulsewidth(self.BackRight, 0) 

        # Wait 1 Second
        time.sleep(1) 

        # Set to Maximum Pulse Width
        self.pi.set_servo_pulsewidth(self.FrontLeft, self.MaximumPulseWidth) 
        self.pi.set_servo_pulsewidth(self.FrontRight, self.MaximumPulseWidth) 
        self.pi.set_servo_pulsewidth(self.BackLeft, self.MaximumPulseWidth) 
        self.pi.set_servo_pulsewidth(self.BackRight, self.MaximumPulseWidth) 
        
        # Wait 1 Second
        time.sleep(1) 
        
        # Set to Minimum Pulse Width
        self.pi.set_servo_pulsewidth(self.FrontLeft, self.MinimumPulseWidth) 
        self.pi.set_servo_pulsewidth(self.FrontRight, self.MinimumPulseWidth) 
        self.pi.set_servo_pulsewidth(self.BackLeft, self.MinimumPulseWidth) 
        self.pi.set_servo_pulsewidth(self.BackRight, self.MinimumPulseWidth) 
        
        # Wait 1 Second
        time.sleep(1)

        # Set the fact that we are now armed
        self.armed = True
