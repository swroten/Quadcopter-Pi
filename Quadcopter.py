# Quadcopter Motors

import logging
import sys
import time
import os
import serial

#Launching GPIO library
os.system ("sudo pigpiod")

#Wait 1 Second
time.sleep(1)

#importing GPIO library
import pigpio 

# Define Class for IMU
class Quadcopter:
    def __init__(self):    
        # Assign GPIO to Variable for Reference
        self.front_right_motor_pin = 2 #Front Right Motor - Spins Counter Clock Wise
        self.front_left_motor_pin = 3  #Front Left Motor  - Spins Clock Wise
        self.back_right_motor_pin = 4  #Back Right Motor  - Spins Clock Wise
        self.back_left_motor_pin = 17  #Back Left Motor   - Spins Counter Clock Wise

        # Set ESC Min & Max Values
        self.MinimumPulseWidth = 700  # ESC - Min Value
        self.MaximumPulseWidth = 2000 # ESC - Max Value

        # Set Min & Max Signal
        MinimumSignal = 0
        MaximumSignal = 1000

        # Set Min & Max Achievable RPM
        MinimumRPM = 0
        MaximumRPM = 6300

        # Set the Calibrated Motor PulseWidth Minimum
        FrontRightMinimumPulseWidth = 1230
        FrontLeftMinimumPulseWidth = 1265
        BackRightMinimumPulseWidth = 1325
        BackLeftMinimumPulseWidth = 1250

        # Set the Calibrated Motor PulseWidth Maximum
        FrontRightMaximumPulseWidth = 1680
        FrontLeftMaximumPulseWidth = 1780
        BackRightMaximumPulseWidth = 1751
        BackLeftMaximumPulseWidth = 1719
        
        # Get Variable for Setting Pulses
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(FrontRight, 0) 
        self.pi.set_servo_pulsewidth(FrontLeft, 0) 
        self.pi.set_servo_pulsewidth(BackLeft, 0) 
        self.pi.set_servo_pulsewidth(BackRight, 0)
        
        
    #Scale Specified Value 
    def scale(self, valueIn, baseMin, baseMax, limitMin, limitMax):
        return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)))

    #Find Pulse Width to Achieve Demanded RPM    
    def get_max_pulse_width(self, motor, initialPulseWidth, demandedRpm, minPulseWidth, maxPulseWidth, accuracy):

        # Initialize Variables
        run = True
        step_rate = 1
        pulseWidth = initialPulseWidth
        
        # Arduino On Serial Port
        # Check the Arduino IDE to see what serial port it's attached to
        ser = serial.Serial('/dev/ttyACM0', 9600)

        # flush any junk left in the serial buffer
        ser.flushInput()

        while run:    
            # Wait for Next Reading
            data = ser.readline()
            
            # Get Observed RPM
            observedRpm = int(data)
        
            # Only Care about Accuracy up to Specified Accuracy
            dRpm = int(demandedRpm / pow(10, accuracy))
            oRpm = int(observedRpm / pow(10, accuracy))
        
            # Print Demanded RPM, Observed RPM, and Pulse Width
            print("Demanded RPM = %d" % demandedRpm)
            print("Observed RPM = %d" % observedRpm)
            print("Pulse Width  = %d" % pulseWidth)
            print()
        
            # Iterate Pulse Width 
            if ((oRpm > dRpm) and (pulseWidth > minPulseWidth)):
                # Decrease Pulse Width
                pulseWidth -= step_rate
            elif ((oRpm < dRpm) and (pulseWidth < maxPulseWidth)):
                # Increase Pulse Width
                pulseWidth += step_rate
            elif (oRpm == dRpm):
                # Stop Running
                run = False
            else:
                run = False
                print("Somehow Reached Unreachable Code")

            # Set Pulse Width of motor
            self.pi.set_servo_pulsewidth(motor, pulseWidth)
                    
            # Sleep Thread for 2 seconds - Allow Stabilization of Arduino Readings
            time.sleep(2)
        
        # Set back to Minimum Pulse Width
        self.pi.set_servo_pulsewidth(motor, minPulseWidth)

        # Stop
        stop()
        
        # Return Max Pulse Width
        return pulseWidth
        
    #Step each motor up from minimum to maximum
    def step_from_min_to_max_to_min():

        # Print Set to Minimum
        print("Setting All Motors to Minimum")
        print()

        # Set Initial Values
        signal = 0
        step_rate = 50
        sleep_time = 3
        demanded_rpm = 0
        back_left_signal = 0
        back_right_signal = 0
        front_left_signal = 0
        front_right_signal = 0        
        back_left_pulse_width = 0    
        back_right_pulse_width = 0    
        front_left_pulse_width = 0    
        front_right_pulse_width = 0        
        
        # Arduino On Serial Port
        # Check the Arduino IDE to see what serial port it's attached to
        ser = serial.Serial('/dev/ttyACM0', 9600)

        print("Press any Key when you are ready to begin...")
        inp = raw_input()

        print("Signal,Demanded RPM,Observed RPM,Front Left Pulse Width,Front Right Pulse Width,Back Left Pulse Width,Back Right Pulse Width")
        
        # While less than max
        while (signal < MaximumSignal):       
            # flush any junk left in the serial buffer
            ser.flushInput()
              
            # Set New Signal
            signal += step_rate
                    
            # Get Demanded RPM From Signal
            demanded_rpm = scale(signal, MinimumSignal, MaximumSignal, MinimumRPM, MaximumRPM)
            
            # Get Pulse Width to achieve Demanded RPM
            back_left_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, BackLeftMinimumPulseWidth, BackLeftMaximumPulseWidth)
            back_right_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, BackRightMinimumPulseWidth, BackRightMaximumPulseWidth)
            front_left_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, FrontLeftMinimumPulseWidth, FrontLeftMaximumPulseWidth)
            front_right_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, FrontRightMinimumPulseWidth, FrontRightMaximumPulseWidth)
            
            # Set Speed For Each Motor 
            pi.set_servo_pulsewidth(BackLeft, back_left_pulse_width)
            pi.set_servo_pulsewidth(BackRight, back_right_pulse_width)
            pi.set_servo_pulsewidth(FrontLeft, front_left_pulse_width)
            pi.set_servo_pulsewidth(FrontRight, front_right_pulse_width)

            # Sleep Thread for specified seconds
            time.sleep(sleep_time)
            
            # Wait for Next Reading
            data = ser.readline()
            
            # Get Observed RPM
            observedRpm = int(data)
            
            # Print Current Speed of Motor
            print('{0},{1},{2},{3},{4},{5},{6}'.format(signal, demanded_rpm, observedRpm, front_left_pulse_width, front_right_pulse_width, back_left_pulse_width, back_right_pulse_width))

        # Set Signal to Maximum minus one step
        signal = MaximumSignal

        # While greater than min
        while (signal > MinimumSignal):       
            # flush any junk left in the serial buffer
            ser.flushInput()
            
            # Set New Signal
            signal -= step_rate
                    
            # Get Demanded RPM From Signal
            demanded_rpm = scale(signal, MinimumSignal, MaximumSignal, MinimumRPM, MaximumRPM)
            
            # Get Pulse Width to achieve Demanded RPM
            back_left_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, BackLeftMinimumPulseWidth, BackLeftMaximumPulseWidth)
            back_right_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, BackRightMinimumPulseWidth, BackRightMaximumPulseWidth)
            front_left_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, FrontLeftMinimumPulseWidth, FrontLeftMaximumPulseWidth)
            front_right_pulse_width = scale(demanded_rpm, MinimumRPM, MaximumRPM, FrontRightMinimumPulseWidth, FrontRightMaximumPulseWidth)
            
            # Set Speed For Each Motor 
            pi.set_servo_pulsewidth(BackLeft, back_left_pulse_width)
            pi.set_servo_pulsewidth(BackRight, back_right_pulse_width)
            pi.set_servo_pulsewidth(FrontLeft, front_left_pulse_width)
            pi.set_servo_pulsewidth(FrontRight, front_right_pulse_width)

            # Sleep Thread for specified seconds
            time.sleep(sleep_time)
            
            # flush any junk left in the serial buffer
            ser.flushInput()
            
            # Wait for Next Reading
            data = ser.readline()
            
            # Get Observed RPM
            observedRpm = int(data)
            
            # Print Current Speed of Motor
            print('{0},{1},{2},{3},{4},{5},{6}'.format(signal, demanded_rpm, observedRpm, front_left_pulse_width, front_right_pulse_width, back_left_pulse_width, back_right_pulse_width))

            
        # Set Speed back to Minimum
        pi.set_servo_pulsewidth(BackLeft, BackLeftMinimumPulseWidth)
        pi.set_servo_pulsewidth(BackRight, BackRightMinimumPulseWidth)
        pi.set_servo_pulsewidth(FrontLeft, FrontLeftMinimumPulseWidth)
        pi.set_servo_pulsewidth(FrontRight, FrontRightMinimumPulseWidth)

        # Stop
        stop()
        
        # Notify user of ramping down to minimum
        print("Program is complete...")
        print
        
        return

    #You will use this function to program your ESC if required
    def manual_drive(): 
        print("You have selected manual option so give a value between 0 and you max value")
        while True:
            inp = raw_input()
            if inp == "stop":
                stop()
                break
            elif inp == "control":
                control()
                break
            elif inp == "arm":
                arm()
                break    
            else:
                pi.set_servo_pulsewidth(FrontLeft,inp)
                pi.set_servo_pulsewidth(FrontRight,inp)
                pi.set_servo_pulsewidth(BackLeft,inp)
                pi.set_servo_pulsewidth(BackRight,inp)

    #This is the auto calibration procedure of a normal ESC              
    def calibrate():   
        pi.set_servo_pulsewidth(FrontLeft, 0) 
        pi.set_servo_pulsewidth(FrontRight, 0) 
        pi.set_servo_pulsewidth(BackLeft, 0) 
        pi.set_servo_pulsewidth(BackRight, 0) 
        print("Disconnect the battery and press Enter")
        inp = raw_input()
        if inp == '':
            pi.set_servo_pulsewidth(FrontLeft, MaximumPulseWidth) 
            pi.set_servo_pulsewidth(FrontRight, MaximumPulseWidth) 
            pi.set_servo_pulsewidth(BackLeft, MaximumPulseWidth) 
            pi.set_servo_pulsewidth(BackRight, MaximumPulseWidth)
            print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = raw_input()
            if inp == '':
                pi.set_servo_pulsewidth(FrontLeft, MinimumPulseWidth) 
                pi.set_servo_pulsewidth(FrontRight, MinimumPulseWidth) 
                pi.set_servo_pulsewidth(BackLeft, MinimumPulseWidth) 
                pi.set_servo_pulsewidth(BackRight, MinimumPulseWidth)
                print("You should hear a special tone...")
                time.sleep(7)
                print("Wait...")
                time.sleep (5)
                print("Wait...")
                pi.set_servo_pulsewidth(FrontLeft, 0) 
                pi.set_servo_pulsewidth(FrontRight, 0) 
                pi.set_servo_pulsewidth(BackLeft, 0) 
                pi.set_servo_pulsewidth(BackRight, 0)
                time.sleep(2)
                print("Arming All ESC now...")
                pi.set_servo_pulsewidth(FrontLeft, MinimumPulseWidth) 
                pi.set_servo_pulsewidth(FrontRight, MinimumPulseWidth) 
                pi.set_servo_pulsewidth(BackLeft, MinimumPulseWidth) 
                pi.set_servo_pulsewidth(BackRight, MinimumPulseWidth)
                time.sleep(1)
                print("Entering Control Mode...")
                control() # You can change this to any other function you want
             
    # Control Motors with Increase / Decrease Controls         
    def control(): 
        print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
        time.sleep(1)

        # Set Speed to Empirical Minimum
        FrontRightSpeed = FrontRightMinimumPulseWidth
        FrontLeftSpeed = FrontLeftMinimumPulseWidth
        BackRightSpeed = BackRightMinimumPulseWidth
        BackLeftSpeed = BackLeftMinimumPulseWidth
        
        print("Controls: ")
        print("  Arm                  = arm")
        print("  Manual               = manual")
        print("  Stop                 = stop")
        print("  Small Speed Decrease = a")
        print("  Small Speed Increase = d")
        print("  Big Speed Decrease   = q")
        print("  Big Speed Increase   = e")
        while True:
            # Set Speed
            pi.set_servo_pulsewidth(FrontLeft, FrontLeftSpeed)
            pi.set_servo_pulsewidth(FrontRight, FrontRightSpeed)
            pi.set_servo_pulsewidth(BackLeft, BackLeftSpeed)
            pi.set_servo_pulsewidth(BackRight, BackRightSpeed)
            
            # Print Current Speed of Each Motor
            print("Front Left Speed = %d" % FrontLeftSpeed)
            print("Front Right Speed = %d" % FrontRightSpeed)
            print("Back Left Speed = %d" % BackLeftSpeed)
            print("Back Right Speed = %d" % BackRightSpeed)

            # Get Input
            inp = raw_input()

            # Perform Requested Function
            if inp == "q":
                # Big Speed Decrement
                FrontLeftSpeed -= 100
                FrontRightSpeed -= 100
                BackLeftSpeed -= 100
                BackRightSpeed -= 100
                
            elif inp == "e":
                # Big Speed Increment
                FrontLeftSpeed += 100
                FrontRightSpeed += 100
                BackLeftSpeed += 100
                BackRightSpeed += 100
                
            elif inp == "d":
                # Small Speed Increment
                FrontLeftSpeed += 10
                FrontRightSpeed += 10
                BackLeftSpeed += 10
                BackRightSpeed += 10
                
            elif inp == "a":
                # Small Speed Decrement
                FrontLeftSpeed -= 10
                FrontRightSpeed -= 10
                BackLeftSpeed -= 10
                BackRightSpeed -= 10

            elif inp == "min":
                # Set all Motors to Min Value
                FrontLeftSpeed = FrontLeftMinimumPulseWidth
                FrontRightSpeed = FrontRightMinimumPulseWidth
                BackLeftSpeed = BackLeftMinimumPulseWidth
                BackRightSpeed = BackRightMinimumPulseWidth
                
            elif inp == "max":
                # Set all Motors to Max Value
                FrontLeftSpeed = FrontLeftMaximumPulseWidth
                FrontRightSpeed = FrontRightMaximumPulseWidth
                BackLeftSpeed = BackLeftMaximumPulseWidth
                BackRightSpeed = BackRightMaximumPulseWidth
                
            elif inp == "stop":
                #going for the stop function
                stop()          
                break
            
            elif inp == "manual":
                #going for the manual function
                manual_drive()
                break
            
            elif inp == "arm":
                #going for the arm function
                arm()
                break
            
            else:
                print("Invalid Control Specified, please try again.")

    #This is the arming procedure of an ESC    
    def arm(): 
        print("Connect the battery and press Enter")
        inp = raw_input()    
        if inp == '':
            pi.set_servo_pulsewidth(FrontLeft, 0)
            pi.set_servo_pulsewidth(FrontRight, 0)
            pi.set_servo_pulsewidth(BackLeft, 0)
            pi.set_servo_pulsewidth(BackRight, 0)
            time.sleep(1)
            pi.set_servo_pulsewidth(FrontLeft, MaximumPulseWidth)
            pi.set_servo_pulsewidth(FrontRight, MaximumPulseWidth)
            pi.set_servo_pulsewidth(BackLeft, MaximumPulseWidth)
            pi.set_servo_pulsewidth(BackRight, MaximumPulseWidth)
            time.sleep(1)
            pi.set_servo_pulsewidth(FrontLeft, MinimumPulseWidth)
            pi.set_servo_pulsewidth(FrontRight, MinimumPulseWidth)
            pi.set_servo_pulsewidth(BackLeft, MinimumPulseWidth)
            pi.set_servo_pulsewidth(BackRight, MinimumPulseWidth)
            time.sleep(1)
            control() 

    #This will stop every action your Pi is performing for ESC of course.        
    def stop(): 
        pi.set_servo_pulsewidth(FrontLeft, 0)
        pi.set_servo_pulsewidth(FrontRight, 0)
        pi.set_servo_pulsewidth(BackLeft, 0)
        pi.set_servo_pulsewidth(BackRight, 0)
        pi.stop()
        
        
        