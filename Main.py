# Quadcopter Flying Code
#!/usr/bin/env python2
import Quadcopter
import IMU
import GPS
import Server
import PID
import time
from threading import Thread
#import thread

# Create IMU Class
imu = IMU.IMU()

# Create GPS Class
#gps = GPS.GPS()

# Create Quadcopter
quad = Quadcopter.Quadcopter()

# Create Reference to PID Variables
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

# Create limits for integral
integral_min = -1
integral_max = 1

# Create PIDs
yawPID = PID.PID(cYawKp, cYawKi, cYawKd, integral_min, integral_max)
rollPID = PID.PID(cRollKp, cRollKi, cRollKd, integral_min, integral_max)
pitchPID = PID.PID(cPitchKp, cPitchKi, cPitchKd, integral_min, integral_max)
throttlePID = PID.PID(cThrottleKp, cThrottleKi, cThrottleKd, integral_min, integral_max)

# Create bool for continuing to run
running = True

# Start Server
thread = Thread(target = Server.flaskThread, args = ())
thread.start()

# Sleep for 1 Second
time.sleep(1)

# Disarmed by default
oArmed = False

# Run Forever
while running:
    # Update Current Observed Values
    imu.update()

    # Get Observed Values    
    oRoll = imu.get_scaled_roll()
    oPitch = imu.get_scaled_pitch()
    oYaw = imu.get_scaled_yaw()
    oThrottle = quad.get_scaled_thrust()    
    #oArmed = quad.get_is_armed()

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

    # Get Commanded Values
    cArm = Server.commands['Armed']
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
    
    # Update all of the PID Loops
    rollOutput = rollPID.update(cRoll, oRoll)
    pitchOutput = pitchPID.update(cPitch, oPitch)
    yawOutput = yawPID.update(cYaw, oYaw)
    throttleOutput = throttlePID.update(abs(cThrottle), oThrottle)
    
    # Print Demanded Output
    #print("Demanded Output -> Roll: {0:0.2F}, Pitch: {1:0.2F}, Yaw: {2:0.2F}, Thrust: {3:0.2F}".format(
    #    rollOutput, pitchOutput, yawOutput, throttleOutput))
    
    # Step Motors in response to Demanded Output
    quad.process_flight_states(throttleOutput, rollOutput, pitchOutput, yawOutput)

    # Get  Updated PID Error Values
    oRollError = rollPID.getError()
    oPitchError = pitchPID.getError()
    oYawError = yawPID.getError()
    oThrottleError = throttlePID.getError()
    
    # Arm if Commanded
    if (cArm):
        # Arm
        oArmed = True
        #quad.arm()
        
    elif (oArmed):
        # Stop
        oArmed = False
        #quad.stop()
        
    # Check if User Demanded to Stop Running
    running = (not Server.commands['Exit'])

    # if no longer running, stop motors
    if (not running):
        quad.stop()
    
    # Sleep for 5 Second
    time.sleep(1)

    # Print Line
    print

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
