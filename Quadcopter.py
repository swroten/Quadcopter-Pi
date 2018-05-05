# Quadcopter Motors
#!/usr/bin/env python2
import logging
import sys
import time
import os
import serial
import math
import numpy as np

#Launching GPIO library
os.system ("sudo pigpiod")

#Wait 1 Second
time.sleep(1)

#importing GPIO library
import pigpio 

# Define Class for Quadcopter Control
class Quadcopter:

    # Initialize
    def __init__(self):        
        # Set as disarmed
        self.armed = False

        # Set Environment conditions
        self.gravity = 9.81 # m/s^2
        self.drag = np.matrix(([0.2],[0.2],[0.2]))
        
        # Set Quadcopter Features
        self.mass = 1.27006      # kg
        self.motor_mass = 0.075  # kg
        self.arm_length = 0.2286 # meters
        self.torque = 0.0        # N*L

        # Get Moment of Interia - modeled mass center as sphere I = (2/5 * M * R^2)
        mass_center = (2.0/5.0)*(0.8)*(0.06)*(0.06)
        inertia_x = float(mass_center + (2 * self.arm_length * self.arm_length * self.motor_mass))
        inertia_y = float(mass_center + (2 * self.arm_length * self.arm_length * self.motor_mass))
        inertia_z = float(mass_center + (4 * self.arm_length * self.arm_length * self.motor_mass))
        self.inertia = np.matrix(([inertia_x,0.0,0.0],[0.0,inertia_y,0.0],[0.0,0.0,inertia_z]))
        self.inertia_inverse =  np.matrix(([(1/inertia_x),0.0,0.0],[0.0,(1/inertia_y),0.0],[0.0,0.0,(1/inertia_z)]))
        
        # Equations of State
        self.up_vector = np.matrix(([0.0],[0.0],[0.0]))
        self.direction_vector = np.matrix(([0.0],[0.0],[0.0]))
        self.position = np.matrix(([0.0],[0.0],[0.0]))
        self.velocity = np.matrix(([0.0],[0.0],[0.0]))
        self.acceleration = np.matrix(([0.0],[0.0],[0.0]))
        self.theta = np.matrix(([0.0],[0.0],[0.0]))
        self.thetadot = np.matrix(([0.0],[0.0],[0.0]))
        
        # Scaling Limits
        self.OutputMinimum = -1
        self.OutputMaximum = 1
        
        # Assign GPIO to Variable for Reference
        self.FrontRight = 2 #Front Right Motor - Spins Counter Clock Wise
        self.FrontLeft = 3  #Front Left Motor  - Spins Clock Wise
        self.BackRight = 4  #Back Right Motor  - Spins Clock Wise
        self.BackLeft = 17  #Back Left Motor   - Spins Counter Clock Wise

        # Set ESC Min & Max Values
        self.MinimumPulseWidth = 700  # ESC - Min Value
        self.MaximumPulseWidth = 2000 # ESC - Max Value

        # Set Min & Max Signal
        self.MinimumSignal = 0
        self.MaximumSignal = 1000

        # Set Min & Max Achievable RPM
        self.MinimumRPM = 0
        self.MaximumRPM = 6300

        # Set Min & Max Thrust
        self.MinimumThrust = 0.0
        self.MaximumThrust = 4 * (0.000000124736 * self.MaximumRPM * self.MaximumRPM)

        # Set the Calibrated Motor PulseWidth Minimum
        self.FrontRightMinimumPulseWidth = 1230
        self.FrontLeftMinimumPulseWidth = 1265
        self.BackRightMinimumPulseWidth = 1325
        self.BackLeftMinimumPulseWidth = 1250

        # Set the Calibrated Motor PulseWidth Maximum
        self.FrontRightMaximumPulseWidth = 1680
        self.FrontLeftMaximumPulseWidth = 1780
        self.BackRightMaximumPulseWidth = 1751
        self.BackLeftMaximumPulseWidth = 1719
        
        # Get Variable for Setting Pulses
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(self.FrontRight, 0) 
        self.pi.set_servo_pulsewidth(self.FrontLeft, 0) 
        self.pi.set_servo_pulsewidth(self.BackRight, 0)
        self.pi.set_servo_pulsewidth(self.BackLeft, 0) 

        # Create Current Variables for Pulse Width
        self.FrontRightPulseWidth = 0
        self.FrontLeftPulseWidth = 0
        self.BackRightPulseWidth = 0
        self.BackLeftPulseWidth = 0
        
        # Create Current Variables for Scaled Pulse Width
        self.FrontRightScaledPulseWidth = 0
        self.FrontLeftScaledPulseWidth = 0
        self.BackRightScaledPulseWidth = 0
        self.BackLeftScaledPulseWidth = 0

        # Create Variables for RPM
        self.FrontRightRPM = 0
        self.FrontLeftRPM = 0
        self.BackRightRPM = 0
        self.BackLeftRPM = 0

        # Create Variables for Thrust
        self.FrontRightThrust = 0
        self.FrontLeftThrust = 0
        self.BackRightThrust = 0
        self.BackLeftThrust = 0

        # Set Minimum Throttle Threshold
        self.minimum_throttle = 0.01

        # Set Last Update Time
        self.last_update = time.time()

    # Get Whether Armed
    def get_is_armed(self):
        return self.armed
        
    # Scale Specified Value 
    def scale(self, valueIn, baseMin, baseMax, limitMin, limitMax):
        # return Scaled Value
        return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)))

    # Compute Static Thrust of a particular motor
    def compute_motor_thrust(self, rpm):
        return (0.000000124736 * rpm * rpm)

    # Compute Resultant Vector for all motors
    def compute_resultant_vector(self):
        # Get RPM for each Motor
        self.FrontLeftRPM = self.scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        self.FrontRightRPM = self.scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        self.BackLeftRPM = self.scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)
        self.BackRightRPM = self.scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.MinimumRPM, self.MaximumRPM)

        # Get Thrust for each Motor
        self.FrontLeftThrust = self.compute_motor_thrust(self.FrontLeftRPM)
        self.FrontRightThrust = self.compute_motor_thrust(self.FrontRightRPM)
        self.BackLeftThrust = self.compute_motor_thrust(self.BackLeftRPM)
        self.BackRightThrust = self.compute_motor_thrust(self.BackRightRPM)

        # Return resultant vector
        return (self.FrontLeftThrust + self.FrontRightThrust + self.BackLeftThrust + self.BackRightThrust)

    # Get Theoretical Raw Roll
    def get_raw_roll(self):
        return min(90.0, max(-90.0, math.degrees(self.theta.item(0) % (2 * math.pi))))

    # Get Theoretical Raw Pitch
    def get_raw_pitch(self):
        return min(180.0, max(-180.0, math.degrees(self.theta.item(1) % (2 * math.pi))))

    # Get Theoretical Raw Yaw
    def get_raw_yaw(self):
        return math.degrees(self.theta.item(2) % (2 * math.pi))

    # Get Theoretical Raw Throttle
    def get_raw_thrust(self):
        return self.compute_resultant_vector()

    # Get Theoretical Scaled Roll
    def get_scaled_roll(self):
        # Initialize Raw Roll - convert from radians to degrees
        raw_roll = self.get_raw_roll()
        
        # Initialize Scaled Roll
        scaled_roll = self.scale(raw_roll, -90.0, 90.0, -1.0, 1.0)

        # return a value between -1.0 and 1.0
        return min(1.0, max(-1.0, scaled_roll))

    # Get Theoretical Scaled Pitch
    def get_scaled_pitch(self):
        # Initialize Raw Pitch - convert from radians to degrees
        raw_pitch = self.get_raw_pitch()
        
        # Initialize Scaled Pitch
        scaled_pitch = self.scale(raw_pitch, -180.0, 180.0, -1.0, 1.0)

        # return a value between -1.0 and 1.0
        return min(1.0, max(-1.0, scaled_pitch))

    # Get Theoretical Scaled Yaw
    def get_scaled_yaw(self):
        # Initialize Raw Yaw - convert from radians to degrees
        raw_yaw = self.get_raw_yaw()
        
        # Initialize Scaled Yaw
        scaled_yaw = 0.0

        # if between 0 and 180 degrees
        if ((raw_yaw > 0.001) and (raw_yaw <= 180.0)):
            scaled_yaw = self.scale(raw_yaw, 0.0, 180.0, 0.0, 1.0)
        # otherwise it is between 180 and 360 degrees
        elif ((raw_yaw > 180.0) and (raw_yaw <= 360.0)):
            scaled_yaw = self.scale(raw_yaw, 180.0, 360.0, -1.0, 0.0)
        else:
            scaled_yaw = 0.0

        # return a value between -1.0 and 1.0
        return min(1.0, max(-1.0, scaled_yaw))

    # Get Theoretical Scaled Throttle
    def get_scaled_thrust(self):
        return self.scale(self.get_raw_thrust(), self.MinimumThrust, self.MaximumThrust, 0.0, self.OutputMaximum)

    #This will stop every action your Pi is performing for ESC of course.        
    def stop(self):
        # if Armed, set pulse width to 0
        if (self.armed):
            self.pi.set_servo_pulsewidth(self.FrontRight, 0)
            self.pi.set_servo_pulsewidth(self.FrontLeft, 0)
            self.pi.set_servo_pulsewidth(self.BackLeft, 0)
            self.pi.set_servo_pulsewidth(self.BackRight, 0)
            
        # Disable any Further Signals
        self.pi.stop()

        # Clear Armed Flag
        self.armed = False

    # Print RPM
    def print_rpm_for_motors(self, roll, pitch, yaw, oRoll, oPitch, oYaw, oThrottle):
        print("RPM -> FL:{3:0.2F},FR:{4:0.2F},BL:{5:0.2F},BR:{6:0.2F},THETA -> R:{0:0.2F},P:{1:0.2F},Y:{2:0.2F},OUT -> R:{0:0.2F},P:{1:0.2F},Y:{2:0.2F},T:{3:0.2F}".format(
            self.FrontLeftRPM, self.FrontRightRPM, self.BackLeftRPM, self.BackRightRPM, roll, pitch, yaw, oRoll, oPitch, oYaw, oThrottle))   

    def compute_rotation(self, roll, pitch, yaw):
        return np.matrix(([ math.cos(yaw)*math.cos(pitch), math.cos(yaw)*math.sin(pitch)*math.sin(roll)-math.sin(yaw)*math.cos(roll), math.cos(yaw)*math.sin(pitch)*math.cos(roll)+math.sin(yaw)*math.sin(roll) ],
                          [ math.sin(yaw)*math.cos(pitch), math.sin(yaw)*math.sin(pitch)*math.sin(roll)+math.cos(yaw)*math.cos(roll), math.sin(yaw)*math.sin(pitch)*math.cos(roll)-math.cos(yaw)*math.sin(roll) ],
                          [ (-1)*math.sin(pitch), math.cos(pitch)*math.sin(roll), math.cos(pitch)*math.cos(roll) ]))

    # Compute Angular Rotation (Local)
    def compute_omega(self, thetadot, roll, pitch):

        # Get Angles Relative to Global Frame
        angles = np.matrix(([1.0, 0.0, (-1)*math.sin(pitch) ],
                            [0.0, math.cos(roll), math.cos(pitch)*math.sin(roll) ],
                            [0.0, (-1)*math.sin(roll), math.cos(pitch)*math.cos(roll) ]))

        # Return Angular Rotation
        return (angles * thetadot)

    # Compute Angular Rotation (Global)
    def compute_thetadot(self, omega, roll, pitch):

        # Get Angles Relative to Local Frame
        angles = np.matrix(([ 1.0, math.sin(roll)*math.tan(pitch), math.cos(roll)*math.tan(pitch) ],
                            [ 0.0, math.cos(roll), (-1)*math.sin(roll) ],
                            [ 0.0, math.sin(roll)/math.cos(pitch), math.cos(roll)/math.cos(pitch) ]))

        # Return Angular Rotation
        return (angles * omega)

    # Update Flight States
    def update(self):
        # Compute delta_time
        delta_time = (time.time() - self.last_update)

        # recall last update time
        self.last_update = time.time()
        
        # Create matrix for gravity
        gravity = np.matrix(([0.0],[0.0],[self.gravity]))

        # Compute Thrust
        thrust = np.matrix(([0.0],[0.0],[self.get_raw_thrust()]))

        # Compute Rotation
        rotation = self.compute_rotation(self.theta.item(0), self.theta.item(1), self.theta.item(2))

        # Compute Localized Thrust
        thrust_local = (rotation * thrust)

        # Compute Drag
        force_drag = np.matrix(([self.drag.item(0)*self.velocity.item(0)], [self.drag.item(1)*self.velocity.item(1)], [self.drag.item(2)*self.velocity.item(2)]))

        # Compute Acceleration
        self.acceleration = (1/self.mass)*(thrust_local-force_drag) - (gravity)

        # Update Velocity
        self.velocity = self.velocity + delta_time * self.acceleration

        # Update Position
        self.position = self.position + delta_time * self.velocity

        # Get Angular Velocities
        omega = self.compute_omega(self.thetadot, self.theta.item(0), self.theta.item(1))

        # Compute Torque generated by motors
        torque_x = ((self.arm_length / math.sqrt(2)) * ((self.FrontRightThrust + self.BackRightThrust) - (self.FrontLeftThrust + self.BackLeftThrust))) # Roll
        torque_y = ((self.arm_length / math.sqrt(2)) * ((self.FrontLeftThrust + self.FrontRightThrust) - (self.BackLeftThrust + self.BackRightThrust))) # Pitch
        torque_z = ((self.FrontLeftThrust + self.BackRightThrust) - (self.BackLeftThrust + self.FrontRightThrust))                                      # Yaw
        self.torque = np.matrix(([torque_x], [torque_y], [torque_z]))       
                                   
        # Compute Angular Accelerations
        inertia_omega_product = self.inertia * omega
        vector_omega = np.matrix(([omega.item(0), omega.item(1), omega.item(2)]))
        vector_product = np.matrix(([inertia_omega_product.item(0), inertia_omega_product.item(1), inertia_omega_product.item(2)]))
        vector_cross_product = (np.cross(vector_omega, vector_product))
        matrix_cross_product = np.matrix(([vector_cross_product.item(0), vector_cross_product.item(1), vector_cross_product.item(2)]))
        omegadot = (self.inertia_inverse * (self.torque - matrix_cross_product))
        
        # Update Angular Velocity
        omega = omega + (delta_time * omegadot)
        self.thetadot = self.compute_thetadot(omega, self.theta.item(0), self.theta.item(1))
        
        # Update Angle
        self.theta = self.theta + (delta_time * self.thetadot)
        
        # Compute Rotation (Again)
        rotation = self.compute_rotation(self.theta.item(0), self.theta.item(1), self.theta.item(2))

        # Get Directional Vector
        self.direction_vector = (rotation * np.matrix(([1],[0],[0])))

        # Get Updward Direction Vector
        self.up_vector = (rotation * np.matrix(([0],[0],[1])))
        
    # Process Commanded States versus Observed States to Step Motors
    def process_flight_states(self, throttleOutput, rollOutput, pitchOutput, yawOutput):       

        # Only Perform standard flight if above minimum throttle threshold
        if (throttleOutput >  self.minimum_throttle):
            # Get Demanded Outputs
            frontLeftOutput = (throttleOutput + rollOutput - pitchOutput - yawOutput)
            frontRightOutput = (throttleOutput - rollOutput - pitchOutput + yawOutput)
            backRightOutput = (throttleOutput - rollOutput + pitchOutput - yawOutput)
            backLeftOutput = (throttleOutput + rollOutput + pitchOutput + yawOutput)
                        
            # Handle Front Left
            frontLeftDemandedOutput = self.scale(frontLeftOutput, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
            self.FrontLeftScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, frontLeftDemandedOutput))
            self.FrontLeftPulseWidth = self.scale(self.FrontLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontLeftMinimumPulseWidth, self.FrontLeftMaximumPulseWidth)

            # Handle Front Right
            frontRightDemandedOutput = self.scale(frontRightOutput, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
            self.FrontRightScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, frontRightDemandedOutput))
            self.FrontRightPulseWidth = self.scale(self.FrontRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.FrontRightMinimumPulseWidth, self.FrontRightMaximumPulseWidth)
                
            # Handle Back Left
            backLeftDemandedOutput = self.scale(backLeftOutput, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
            self.BackLeftScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, backLeftDemandedOutput))
            self.BackLeftPulseWidth = self.scale(self.BackLeftScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackLeftMinimumPulseWidth, self.BackLeftMaximumPulseWidth)
                
            # Handle Back Right
            backRightDemandedOutput = self.scale(backRightOutput, 0.0, self.OutputMaximum, self.MinimumSignal, self.MaximumSignal)
            self.BackRightScaledPulseWidth = max(self.MinimumSignal, min(self.MaximumSignal, backRightDemandedOutput))
            self.BackRightPulseWidth = self.scale(self.BackRightScaledPulseWidth, self.MinimumSignal, self.MaximumSignal, self.BackRightMinimumPulseWidth, self.BackRightMaximumPulseWidth)
        
            # Set Pulse Width Signal if Motors are Armed
            if (self.armed):
                self.pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftPulseWidth)
                self.pi.set_servo_pulsewidth(self.FrontRight, self.FrontRightPulseWidth)
                self.pi.set_servo_pulsewidth(self.BackLeft, self.BackLeftPulseWidth)
                self.pi.set_servo_pulsewidth(self.BackRight, self.BackRightPulseWidth)
        else:
            # Set Minimum Threshold            
            self.pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftMinimumPulseWidth)
            self.pi.set_servo_pulsewidth(self.FrontRight, self.FrontRightMinimumPulseWidth)
            self.pi.set_servo_pulsewidth(self.BackLeft, self.BackLeftMinimumPulseWidth)
            self.pi.set_servo_pulsewidth(self.BackRight, self.BackRightMinimumPulseWidth)                    
        
    # Arming Procedure for all ESC    
    def arm(self): 
        # Set to 0
        self.pi.set_servo_pulsewidth(self.FrontLeft, self.FrontLeftMinimumPulseWidth)
        self.pi.set_servo_pulsewidth(self.FrontRight, self.FrontRightMinimumPulseWidth)
        self.pi.set_servo_pulsewidth(self.BackLeft, self.BackLeftMinimumPulseWidth)
        self.pi.set_servo_pulsewidth(self.BackRight, self.BackRightMinimumPulseWidth)

        # Wait 1 Second
        time.sleep(1)

        # Set the fact that we are now armed
        self.armed = True

    # Perform Landing Routine
    def land(self, throttleOutput):
        # Set landing Flag
        landing = True

        # Initialize Demanded Throttle
        dThrottle = throttleOutput

        # Set current throttle output to initial
        tOut = throttleOutput

        # Set step rate
        step_rate = 0.01

        # Set update rate
        update_rate = 1

        # Set last update time
        last_update = time.time()

        # Get the Observed Throttle
        oThrottle = self.get_scaled_thrust()

        # While Landing
        while (landing):

            # Check if it is time to update again
            if ((time.time() - last_update) > update_rate):
                # Recall Now as last update time
                last_update = time.time()
            
                # Decrement current Throttle Output
                tOut -= step_rate

                # Get the Observed Throttle
                oThrottle = self.get_scaled_thrust()

                # Compute Error
                error = abs(tOut - oThrottle)

                # Set Demanded Throttle
                dThrottle -= (step_rate * error)

                # Make sure that Throttle doesn't fall below 0
                dThrottle = max(0.0, dThrottle)
        
                # Process Flight States
                self.process_flight_states(dThrottle, 0, 0, 0)
        
                # Print something for debugging
                print("Updated Demanded Throttle: ", oThrottle)
                      
            # continue landing while demanded throttle isn't at minimum
            landing = (oThrottle > self.minimum_throttle)
        
