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
        self.MaximumThrust = (0.000000124736 * self.MaximumRPM * self.MaximumRPM)

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

        # Recall Last Throttle
        self.last_raw_throttle = 0.0

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
        front_left_rpm = self.scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        front_right_rpm = self.scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        back_left_rpm = self.scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        back_right_rpm = self.scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)

        # Get Thrust for each Motor
        front_left_thrust = self.compute_motor_thrust(front_left_rpm)
        front_right_thrust = self.compute_motor_thrust(front_right_rpm)
        back_left_thrust = self.compute_motor_thrust(back_left_rpm)
        back_right_thrust = self.compute_motor_thrust(back_right_rpm)

        # Get the resultant vector
        return math.sqrt((front_left_thrust * front_left_thrust) +
                         (front_right_thrust * front_right_thrust) + 
                         (back_left_thrust * back_left_thrust) + 
                         (back_right_thrust * back_right_thrust))


    # Get Observed Raw Throttle
    def get_raw_throttle(self):
        return self.compute_resultant_vector()

    # Get Observed Scaled Throttle
    def get_scaled_throttle(self):
        return self.scale(self.get_raw_throttle(), self.MinimumThrust, self.MaximumThrust, -1.0, 1.0)

    #This will stop every action your Pi is performing for ESC of course.        
    def stop(self): 
        pi.set_servo_pulsewidth(self.FrontRight, 0)
        pi.set_servo_pulsewidth(self.FrontLeft, 0)
        pi.set_servo_pulsewidth(self.BackLeft, 0)
        pi.set_servo_pulsewidth(self.BackRight, 0)
        pi.stop()
        self.armed = False

    # Process Commanded States versus Observed States to Step Motors
    def process_flight_states(self, throttleOutput, rollOutput, pitchOutput, yawOutput):
        
        # Get Demanded Output
        frontLeftDemandedOutput = self.scale((throttleOutput + rollOutput - pitchOutput - yawOutput), self.OutputMinimum, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        frontRightDemandedOutput = self.scale((throttleOutput - rollOutput - pitchOutput + yawOutput), self.OutputMinimum, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        backLeftDemandedOutput = self.scale((throttleOutput + rollOutput + pitchOutput + yawOutput), self.OutputMinimum, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        backRightDemandedOutput = self.scale((throttleOutput - rollOutput + pitchOutput - yawOutput), self.OutputMinimum, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
        
        # Handle Front Left
        self.FrontLeftScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, frontLeftDemandedOutput))
        self.FrontLeftPulseWidth = self.scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontLeftMinimumPulseWidth, self.FrontLeftMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftPulseWidth)

        # Handle Front Right
        self.FrontRightScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, frontRightDemandedOutput))
        self.FrontRightPulseWidth = self.scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontRightMinimumPulseWidth, self.FrontRightMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.FrontRight, self.FrontRightPulseWidth)
        
        # Handle Back Left
        self.BackLeftScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, backLeftDemandedOutput))
        self.BackLeftPulseWidth = self.scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackLeftMinimumPulseWidth, self.BackLeftMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.BackLeft, self.BackLeftPulseWidth)
        
        # Handle Back Right
        self.BackRightScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, backRightDemandedOutput))
        self.BackRightPulseWidth = self.scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackRightMinimumPulseWidth, self.BackRightMaximumPulseWidth)
        #pi.set_servo_pulsewidth(self.BackRight, self.BackRightPulseWidth)

        # Print Pulse Width
        print("Demanded Output -> FL: {0:0.2F}, FR: {1:0.2F}, BL: {2:0.2F}, BR: {3:0.2F}".format(
        frontLeftDemandedOutput,
        frontRightDemandedOutput,
        backLeftDemandedOutput,
        backRightDemandedOutput))

        # Print Pulse Width
        #print("Pulse Width     -> FL: {0:0.2F}, FR: {1:0.2F}, BL: {2:0.2F}, BR: {3:0.2F}".format(
        #self.FrontLeftScaledPulseWidth,
        #self.FrontRightScaledPulseWidth,
        #self.BackLeftScaledPulseWidth,
        #self.BackRightScaledPulseWidth))
        
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

        # Set the fact that we are now armed
        self.armed = True
