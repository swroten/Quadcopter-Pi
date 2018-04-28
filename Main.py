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
oRollKi = 1.0 
oRollKp = 50.0 
oRollKd = 1.0
oRollError = 0.0
oPitchKi = 1.0 
oPitchKp = 50.0 
oPitchKd = 1.0 
oPitchError = 0.0
oYawKi = 1.0 
oYawKp = 50.0 
oYawKd = 1.0 
oYawError = 0.0
oThrottleKi = 1.0 
oThrottleKp = 50.0 
oThrottleKd = 1.0
oThrottleError = 0.0

# Create limits for integral
integral_min = 0
integral_max = 1000

# Create PIDs
yawPID = PID.PID(oYawKp, oYawKi, oYawKd, integral_min, integral_max)
rollPID = PID.PID(oRollKp, oRollKi, oRollKd, integral_min, integral_max)
pitchPID = PID.PID(oPitchKp, oPitchKi, oPitchKd, integral_min, integral_max)
throttlePID = PID.PID(oThrottleKp, oThrottleKi, oThrottleKd, integral_min, integral_max)

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
    oThrottle = quad.get_scaled_throttle()    
    #oArmed = quad.get_is_armed()

    # Update Observed Values in Server
    Server.observed['Armed'] = oArmed
    Server.observed['Roll'] = oRoll
    Server.observed['RollKp'] = oRollKp
    Server.observed['RollKi'] = oRollKi
    Server.observed['RollKd'] = oRollKd
    Server.observed['RollError'] = oRollError
    Server.observed['Pitch'] = oPitch
    Server.observed['PitchKp'] = oPitchKp
    Server.observed['PitchKi'] = oPitchKi
    Server.observed['PitchKd'] = oPitchKd
    Server.observed['PitchError'] = oPitchError
    Server.observed['Yaw'] = oYaw
    Server.observed['YawKp'] = oYawKp
    Server.observed['YawKi'] = oYawKi
    Server.observed['YawKd'] = oYawKd
    Server.observed['YawError'] = oYawError
    Server.observed['Throttle'] = oThrottle
    Server.observed['ThrottleKp'] = oThrottleKp
    Server.observed['ThrottleKi'] = oThrottleKi
    Server.observed['ThrottleKd'] = oThrottleKd
    Server.observed['ThrottleError'] = oThrottleError

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
    throttleOutput = throttlePID.update(cThrottle, oThrottle)

    # Step Motors in response to Demanded Output
    #quad

    # Get  Updated PID Error Values
    oRollError = rollPID.getError()
    oPitchError = pitchPID.getError()
    oYawError = yawPID.getError()
    oThrottleError = throttlePID.getError()
    
    # Print Demanded Output
    print("Demanded Output -> Roll: {0:0.2F}, Pitch: {1:0.2F}, Yaw: {2:0.2F}, Thrust: {3:0.2F}".format(
        rollOutput, pitchOutput, yawOutput, thrustOutput))

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
    
    # Sleep for 1 Second
    time.sleep(1)

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
