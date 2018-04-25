# Quadcopter Flying Code

import Quadcopter
import IMU
import GPS
import Server
import FlightControl
import PID

# Create GPS Class
gps = GPS.GPS()

# Create Quadcopter
quad = Quadcopter.Quadcopter()

# Create PIDs
rollPID = PID.PID(1, 1, 1, 0, 1000)
pitchPID = PID.PID(1, 1, 1, 0, 1000)
yawPID = PID.PID(1, 1, 1, 0, 1000)
thrustPID = PID.PID(1, 0, 0, 0, 1000)

# Create Server
from Server.flask import *

# Start Server
app.run()

# Run Forever
while True:
    # Get Observed and Commanded Values
    cRoll = Server.commands['Roll']
    cPitch = Server.commands['Pitch']
    cYaw = Server.commands['Yaw']


    # Update all of the PID Loops
    rollPID.update()


# Stop Server
app.stop()

# Close Program
print('Program Exiting...')
