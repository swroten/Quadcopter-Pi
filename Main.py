# Quadcopter Flying Code

import Quadcopter
import IMU
import GPS

print("For first time launch, select calibrate")
print("Type the exact word for the function you want")
print("imu or gps or calibrate OR manual OR control OR arm OR stop")

# Create Quadcopter
quad = Quadcopter.Quadcopter()

# Run Forever
while True:
    # Get Input From User
    inp = raw_input()    
    
    # Perform function based on input
    if inp == "manual":
        # Perform Manual Drive Function 
        quad.manual_drive()
    elif inp == "calibrate":
        # Perform Calibrate Drive Function
        quad.calibrate()
    elif inp == "arm":
        # Perform Arm Drive Function
        quad.arm()
    elif inp == "control":
        # Perform Control Drive Function
        quad.control()    
    elif inp == "imu":
        # Create IMU Class
        imu = IMU.IMU()
        
        # Print IMU
        imu.PrintIMUValues()
        
    elif inp == "gps":
        # Create GPS Class
        gps = GPS.GPS()
        
        # Print GPS
        gps.PrintGPS()
    
    elif inp == "frontleftmaxpulsewidth":
        # Set all Other Motors to Max Speed
        pi.set_servo_pulsewidth(BackLeft, BackLeftMaximumPulseWidth)
        pi.set_servo_pulsewidth(BackRight, BackRightMaximumPulseWidth)
        pi.set_servo_pulsewidth(FrontRight, FrontRightMaximumPulseWidth)
        
        # Get Pulse Width to Achieve Selected Max RPM        
        frontLeftMaxPulseWidth = get_max_pulse_width(FrontLeft, FrontLeftMaximumPulseWidth, MaximumRPM, FrontLeftMinimumPulseWidth, MaximumPulseWidth, 1)
    
        # Print Max Pulse Width
        print("Front Left Max Pulse Width: %d" % frontLeftMaxPulseWidth)
            
        # Break
        break
    elif inp == "frontrightmaxpulsewidth":
        # Set all Other Motors to Max Speed
        pi.set_servo_pulsewidth(BackLeft, BackLeftMaximumPulseWidth)
        pi.set_servo_pulsewidth(BackRight, BackRightMaximumPulseWidth)
        pi.set_servo_pulsewidth(FrontLeft, FrontLeftMaximumPulseWidth)
        
        # Get Pulse Width to Achieve Selected Max RPM
        frontRightMaxPulseWidth = get_max_pulse_width(FrontRight, FrontRightMaximumPulseWidth, MaximumRPM, FrontRightMinimumPulseWidth, MaximumPulseWidth, 1)
    
        # Print Max Pulse Width
        print("Front Right Max Pulse Width: %d" % frontRightMaxPulseWidth)
        
        # Break
        break
    elif inp == "backleftmaxpulsewidth":
        # Set all Other Motors to Max Speed
        pi.set_servo_pulsewidth(BackRight, BackRightMaximumPulseWidth)
        pi.set_servo_pulsewidth(FrontLeft, FrontLeftMaximumPulseWidth)
        pi.set_servo_pulsewidth(FrontRight, FrontRightMaximumPulseWidth)
        
        # Get Pulse Width to Achieve Selected Max RPM
        backLeftMaxPulseWidth = get_max_pulse_width(BackLeft, BackLeftMaximumPulseWidth, MaximumRPM, BackLeftMinimumPulseWidth, MaximumPulseWidth, 1)
    
        # Print Max Pulse Width
        print("Back Left Max Pulse Width: %d" % backLeftMaxPulseWidth)
        
        # Break
        break
    elif inp == "backrightmaxpulsewidth":
        # Set all Other Motors to Max Speed
        pi.set_servo_pulsewidth(BackLeft, BackLeftMaximumPulseWidth)
        pi.set_servo_pulsewidth(FrontLeft, FrontLeftMaximumPulseWidth)
        pi.set_servo_pulsewidth(FrontRight, FrontRightMaximumPulseWidth)
        
        # Get Pulse Width to Achieve Selected Max RPM
        backRightMaxPulseWidth = get_max_pulse_width(BackRight, BackRightMaximumPulseWidth, MaximumRPM, BackRightMinimumPulseWidth, MaximumPulseWidth, 1)
    
        # Print Max Pulse Width
        print("Back Right Max Pulse Width: %d" % backRightMaxPulseWidth)
        
        # Break
        break
    elif inp == "step":
        step_from_min_to_max_to_min()
        break
    elif inp == "stop":
        stop()
        break
    else:
        print('Program Exiting...')
        break
