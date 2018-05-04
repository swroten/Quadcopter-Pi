# Quadcopter-Pi
Quadcopter with Raspberry Pi as Flight Controller using Python

# Steps to Run
1. Make sure you start GPS Module before Starting Quadcopter
    sudo gpsd /dev/ttyACM0 -F /var/run/gpsd.sock
2. chmod a+x Main.py
3. ./Main.py
4. If errors encountered while reading IMU - exit and restart
5. To Cancel: cntrl-\ and then type sudo killall pigpiod
6. 
  
