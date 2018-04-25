#!/usr/bin/env python2
import time

# PID Controller
class PID:
    # Initialize
    def __init__(self, kp, ki, kd, integral_min, integral_max):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0.0
        self.proportional_term = 0.0
        self.integral_term = 0.0
        self.derivative_term = 0.0
        self.integral_min = integral_min
        self.integral_max = integral_max
        self.setpoint = 0.0
        self.current = 0.0
        self.output = 0.0
        self.dt = 0.0
        self.last_time = 0.0
        self.last_error = 0.0
        self.last_derivative = 0.0
        self.filter = 0.0

    def getError(self):
        return self.error

    def setProportionalConstant(self, kp):
        self.kp = kp
        
    def setIntegralConstant(self, ki):
        self.ki = ki

    def setDerivativeConstant(self, kd):
        self.kd = kd

    def setSetpoint(self, setpoint):
        self.setpoint = setpoint

    # Perform Update from Current Value
    def update(self, current):
        # Update Current Value
        self.current = current
        
        # Update Time Since Last Update
        self.dt = (time.time() - self.last_time)

        # Recall Last Update Time
        self.last_time = time.time()

        # Calculate Error
        self.error = self.setpoint - self.current

        # Compute Proportional Term
        self.proportional_term = (self.kp * self.error)

        # Compute Integral Term
        self.integral_term = (self.integral_term + (self.ki * self.error * self.dt))

        # Make sure Integral Term is within Min and Max
        if (self.integral_term < self.integral_min):
            self.integral_term = self.integral_min
        elif (self.integral_term > self.integral_max):
            self.integral_term = self.integral_max
            
        # Compute Derivative
        self.derivative_term = (self.kd * ((((self.error - self.last_error) / self.dt) * self.filter) + 
            (self.last_derivative * (1 - self.filter))))
                
        # Recall Last Error and Derivative
        self.last_error = self.error
        self.last_derivative = self.derivative_term
        
        # Compute Output
        self.output = (self.proportional_term + self.integral_term + self.derivative_term)

        # Return Output
        return self.output


