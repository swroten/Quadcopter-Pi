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

# Create PIDs
rollPID = PID.PID(50, 1, 1, 0, 1000)
pitchPID = PID.PID(50, 1, 1, 0, 1000)
yawPID = PID.PID(50, 1, 1, 0, 1000)
thrustPID = PID.PID(1, 0, 0, 0, 1000)

# Create bool for continuing to run
running = True

# Start Server
thread = Thread(target = Server.flaskThread, args = ())
thread.start()
#threadId = thread.start_new_thread(Server.flaskThread,())
#Server.app.run(threaded=True)

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
    oThrust = quad.get_scaled_throttle()
    #oArmed = quad.get_is_armed()

    # Update Observed Values in Server
    Server.observed['Armed'] = oArmed
    Server.observed['Roll'] = oRoll
    Server.observed['Pitch'] = oPitch
    Server.observed['Yaw'] = oYaw
    Server.observed['Throttle'] = oThrust

    # Get Commanded Values
    cArm = Server.commands['Armed']
    cRoll = Server.commands['Roll']
    cPitch = Server.commands['Pitch']
    cYaw = Server.commands['Yaw']
    cThrust = Server.commands['Throttle']
    
    # Update all of the PID Loops
    rollOutput = rollPID.update(cRoll, oRoll)
    pitchOutput = pitchPID.update(cPitch, oPitch)
    yawOutput = yawPID.update(cYaw, oYaw)
    thrustOutput = thrustPID.update(cThrust, oThrust)
    
    # Print that Server is running
    print("Error           -> Roll: {0:0.2F}, Pitch: {1:0.2F}, Yaw: {2:0.2F}, Thrust: {3:0.2F}".format(
        rollPID.getError(), pitchPID.getError(), yawPID.getError(), thrustPID.getError()))
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
    
    # Sleep for 5 Second
    time.sleep(5)

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
