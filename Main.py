#!/usr/bin/env python2
import Quadcopter
import IMU
import GPS
import Server
import PID
import time
import numpy as np
from threading import Thread
#import thread

try:    
    # Create IMU Class
    imu = IMU.IMU()
except:
    # Write Line to indicate IMU failed to initialize
    print("Error: IMU failed to Initialize! Please try again to start...")

    # Exit
    exit(0)

# Create GPS Class
#gps = GPS.GPS()

# Create Quadcopter
quad = Quadcopter.Quadcopter()

# Create Variables
cSnap = False
cResetError = False

# Create Reference to PID Variables
cYaw = 0.0
rYaw = 0.0
cRoll = 0.0
rRoll = 0.0
cPitch = 0.0
rPitch = 0.0
cThrottle = 0.0
cYawKi = 0.05
cYawKp = 0.10
cYawKd = 0.05 
cRollKi = 0.05 
cRollKp = 0.10
cRollKd = 0.05
cPitchKi = 0.05 
cPitchKp = 0.10 
cPitchKd = 0.05 
cThrottleKi = 0.0
cThrottleKp = 0.1
cThrottleKd = 0.0
oYawError = 0.0
oRollError = 0.0
oPitchError = 0.0
oThrottleError = 0.0
throttleOutput = 0.0

# Set Sample Time
print_rpm_freq = 1.0
pid_sample_time = 0.0

# Create limits for integral
integral_min = -1
integral_max = 1

# Communication Loss Threshold (seconds)
comm_loss_threshold = 60.0

# Create PIDs
yawPID = PID.PID(cYawKp, cYawKi, cYawKd, pid_sample_time, integral_min, integral_max)
rollPID = PID.PID(cRollKp, cRollKi, cRollKd, pid_sample_time, integral_min, integral_max)
pitchPID = PID.PID(cPitchKp, cPitchKi, cPitchKd, pid_sample_time, integral_min, integral_max)
throttlePID = PID.PID(cThrottleKp, cThrottleKi, cThrottleKd, pid_sample_time, integral_min, integral_max)

# Create bool for continuing to run
running = True

# Start Server
thread = Thread(target = Server.flaskThread, args = ())
thread.start()

# Sleep for 1 Second
time.sleep(1)

# Disarmed by default
oArmed = False

# Recall this time as last_time
last_time = time.time()

# Run Forever
while running:
    try:
        # Get Time since last update
        delta_time = (time.time() - last_time)
                
        # Update Current Observed Values
        imu.update()

        # Get Observed Thurst
        oThrottle = quad.get_scaled_thrust() 

        # Update Flight States
        quad.update()

        # Get if Quad is Armed   
        oArmed = quad.get_is_armed()

        # Get Observed Values
        if (oArmed):
            # if we are armed - assume flying
            #  get roll, pitch, and yaw from IMU
            oYaw = imu.get_scaled_yaw()
            oRoll = imu.get_scaled_roll()
            oPitch = imu.get_scaled_pitch()

            # Get Raw Values
            rYaw = imu.get_raw_yaw()
            rRoll = imu.get_raw_roll()
            rPitch = imu.get_raw_pitch()
        else:
            # otherwise - assume in test mode
            #  get roll, pitch and yaw from Quad
            oYaw = quad.get_scaled_yaw()
            oRoll = quad.get_scaled_roll()
            oPitch = quad.get_scaled_pitch()
            
            # Get Raw Values
            rYaw = quad.get_raw_yaw()
            rRoll = quad.get_raw_roll()
            rPitch = quad.get_raw_pitch()
            
        # Update Observed Values in Server
        Server.observed['Armed'] = oArmed
        Server.observed['Yaw'] = oYaw
        Server.observed['Roll'] = oRoll
        Server.observed['Pitch'] = oPitch
        Server.observed['Throttle'] = oThrottle
        Server.observed['YawError'] = oYawError
        Server.observed['RollError'] = oRollError
        Server.observed['PitchError'] = oPitchError
        Server.observed['ThrottleError'] = oThrottleError

        # Update Constants based on Commanded
        Server.observed['Time'] = time.time()
        Server.observed['YawKp'] = cYawKp
        Server.observed['YawKi'] = cYawKi
        Server.observed['YawKd'] = cYawKd   
        Server.observed['RollKp'] = cRollKp
        Server.observed['RollKi'] = cRollKi
        Server.observed['RollKd'] = cRollKd 
        Server.observed['PitchKp'] = cPitchKp
        Server.observed['PitchKi'] = cPitchKi
        Server.observed['PitchKd'] = cPitchKd
        Server.observed['ThrottleKp'] = cThrottleKp
        Server.observed['ThrottleKi'] = cThrottleKi
        Server.observed['ThrottleKd'] = cThrottleKd
        Server.observed['ResetError'] = cResetError
        Server.observed['Snap'] = cSnap
    
        # Get Commanded Values
        cTime = Server.commands['Time']
        cArm = Server.commands['Armed']
        cSnap = Server.commands['Snap']
        cResetError = Server.commands['ResetError']
        cRoll = Server.commands['Roll']
        cRollKi = Server.commands['RollKi']
        cRollKp = Server.commands['RollKp']
        cRollKd = Server.commands['RollKd']
        cPitch = Server.commands['Pitch']
        cPitchKi = Server.commands['PitchKi']
        cPitchKp = Server.commands['PitchKp']
        cPitchKd = Server.commands['PitchKd']
        cYaw = Server.commands['Yaw']
        cYawKi = Server.commands['YawKi']
        cYawKp = Server.commands['YawKp']
        cYawKd = Server.commands['YawKd']
        cThrottle = Server.commands['Throttle']
        cThrottleKi = Server.commands['ThrottleKi']
        cThrottleKp = Server.commands['ThrottleKp']
        cThrottleKd = Server.commands['ThrottleKd']
        
        # Check if Error Should be Reset on PID
        if (cResetError):
            # Reset integral and derivative error
            rollPID.reset()
            pitchPID.reset()
            yawPID.reset()
            throttlePID.reset()

            # Clear this flag
            cResetError = False            

        # Set Commanded PID Constants
        rollPID.setProportionalConstant(cRollKp)
        rollPID.setIntegralConstant(cRollKi)
        rollPID.setDerivativeConstant(cRollKd)
    
        pitchPID.setProportionalConstant(cPitchKp)
        pitchPID.setIntegralConstant(cPitchKi)
        pitchPID.setDerivativeConstant(cPitchKd)
    
        yawPID.setProportionalConstant(cYawKp)
        yawPID.setIntegralConstant(cYawKi)
        yawPID.setDerivativeConstant(cYawKd)
    
        throttlePID.setProportionalConstant(cThrottleKp)
        throttlePID.setIntegralConstant(cThrottleKi)
        throttlePID.setDerivativeConstant(cThrottleKd)

        # Restrict Roll to Min and Max of (+/- 30 degrees)
        cRoll = min(0.33, max(-0.33, cRoll))

        # Restrict Pitch to Min and Max of (+/- 30 degrees)
        cPitch = min(0.33, max(-0.33, cPitch))
    
        # Update all of the PID Loops
        yawOutput = yawPID.update(cYaw, oYaw)
        rollOutput = rollPID.update(cRoll, oRoll)
        pitchOutput = pitchPID.update(cPitch, oPitch)
        throttleOutput = throttlePID.update(abs(cThrottle), oThrottle)
    
        # Step Motors in response to Demanded Output
        quad.process_flight_states(throttleOutput, rollOutput, pitchOutput, yawOutput)

        # Get  Updated PID Error Values
        oYawError = yawPID.getError()
        oRollError = rollPID.getError()
        oPitchError = pitchPID.getError()
        oThrottleError = throttlePID.getError()
    
        # Arm if Commanded
        if (cArm and not oArmed):
            # Arm
            quad.arm()
        
            # Recall it is armed
            oArmed = True
        # Disarm if no longer commanded as Armed
        elif (oArmed and not cArm):
            # Stop
            oArmed = False
            quad.stop()
        
        # Check if User Demanded to Stop Running
        running = (not Server.commands['Exit'])

        # Check if Comm Failure has occurred
        if ((oArmed) and ((time.time() - cTime) > comm_loss_threshold)):
            # Write Line to indicate we are landing
            print("Communication Failure -> Landing...")
            
            # Perform Landing Routine
            quad.land(throttleOutput)

            # Write Line to indicate we have finished landing
            print("Successfully completed landing Routine!")

            # Stop Running
            running = False        

        # if no longer running, stop motors
        if (not running):
           quad.stop()

        # Print Values for RPM if print line time has passed
        if (delta_time > print_rpm_freq):
            # Print RPM for motors
            quad.print_rpm_for_motors(rRoll, rPitch, rYaw, rollOutput, pitchOutput, yawOutput, throttleOutput)
            
            # Recall this time
            last_time = time.time()
            
    except (Exception, KeyboardInterrupt), e:
        # Write Line to indicate some exception occurred
        print("Exception ocurred while running '{0}' -> Landing...".format(str(e)))

        # Perform Landing Routine
        quad.land(throttleOutput)
        
        # Write Line to indicate we have finished landing
        print("Successfully completed landing Routine!")
        
        # Stop Running
        running = False

        # Stop the Motors
        quad.stop()

# Close Program
print('Program Exiting...')

try:    
    # Stop Server
    Server.stop()
except RuntimeError, msg:
    print(msg)

# Close Program
print('Program Has Exited...')

exit(0)
