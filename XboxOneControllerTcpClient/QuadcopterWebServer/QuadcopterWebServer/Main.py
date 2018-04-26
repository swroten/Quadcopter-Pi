# Quadcopter Flying Code

import Quadcopter
import IMU
import GPS
import Server
import FlightControl
import PID

# Create IMU Class
imu = IMU.IMU()

# Create GPS Class
#gps = GPS.GPS()

# Create Quadcopter
quad = Quadcopter.Quadcopter()

# Create PIDs
rollPID = PID.PID(1, 1, 1, 0, 1000)
pitchPID = PID.PID(1, 1, 1, 0, 1000)
yawPID = PID.PID(1, 1, 1, 0, 1000)
thrustPID = PID.PID(1, 0, 0, 0, 1000)

# Create bool for continuing to run
running = True

# Create Server
from Server.flask import *

# Start Server
app.run()

# Run Forever
while running:
    # Update Current Observed Values
    imu.update()

    # Get Observed Values    
    oRoll = imu.get_scaled_roll()
    oPitch = imu.get_scaled_pitch()
    oYaw = imu.get_scaled_yaw()
    oThrust = quad.get_scaled_throttle()

    # Update Observed Values in Server
    Server.observed['Roll'] = oRoll
    Server.observed['Pitch'] = oPitch
    Server.observed['Yaw'] = oYaw
    Server.observed['Throttle'] = oThrust

    # Get Commanded Values
    cRoll = Server.commands['Roll']
    cPitch = Server.commands['Pitch']
    cYaw = Server.commands['Yaw']
    cThrust = Server.commands['Throttle']
    
    # Update all of the PID Loops
    rollOutput = rollPID.update(cRoll, oRoll)
    pitchOutput = pitchPID.update(cPitch, oPitch)
    yawOutput = yawPID.update(cYaw, oYaw)
    thrustOutput = thrustPID.update(cThrust, oThrust)

    # Check if User Demanded to Stop Running
    running = (not Server.commands['Exit'])

# Stop Server
app.stop()

# Close Program
print('Program Exiting...')
