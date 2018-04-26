#!/usr/bin/env python2
import time

# PID Controller
class PID:
    # Initialize
    def __init__(self, kp, ki, kd, min_signal, max_signal):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0.0
        self.proportional_term = 0.0
        self.integral_term = 0.0
        self.derivative_term = 0.0
        self.min_signal = min_signal
        self.max_signal = max_signal
        self.setpoint = 0.0
        self.current = 0.0
        self.output = 0.0
        self.dt = 0.0
        self.last_time = time.time()
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
    def update(self, setpoint, current):
        # Update Current Values
        self.current = current
        self.setpoint = setpoint
        
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
        if (self.integral_term < self.min_signal):
            self.integral_term = self.min_signal
        elif (self.integral_term > self.max_signal):
            self.integral_term = self.max_signal
            
        # Compute Derivative
        self.derivative_term = (self.kd * ((((self.error - self.last_error) / self.dt) * self.filter) + 
            (self.last_derivative * (1 - self.filter))))
                
        # Recall Last Error and Derivative
        self.last_error = self.error
        self.last_derivative = self.derivative_term
        
        # Compute Output
        self.output = (self.proportional_term + self.integral_term + self.derivative_term)
        
        # Make sure Computed Output is within Min and Max
        if (self.output < self.min_signal):
            self.output = self.min_signal
        elif (self.output > self.max_signal):
            self.output = self.max_signal

        # Return Output
        return self.output


