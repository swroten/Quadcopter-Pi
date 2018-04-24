# Quadcopter Flying Code

import Quadcopter
import IMU
import GPS
import Server
import FlightControl

print("For first time launch, select calibrate")
print("Type the exact word for the function you want")
print("imu or gps or calibrate OR manual OR control OR arm OR stop")



# Create GPS Class
gps = GPS.GPS()

# Create Quadcopter
quad = Quadcopter.Quadcopter()

# Create Server
from Server.flask import *

# Start Server
app.run()

# Run Forever
while True:


# Stop Server
app.stop()

# Close Program
print('Program Exiting...')
