import time

class PIDController:

    def __init__(self, setpoint):
        self.setpoint = setpoint
        self.measurement = 0

        self.kP = 0.2
        self.kI = 0
        self.kD = 0

        self.integral = 0
        self.previous_error = 0

        self.last_time = int(round(time.time() * 1000))
    
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def pID(self):
        #calculate time in ms since last called
        current_time = int(round(time.time() * 1000))
        dT = current_time - self.last_time + 1

        #error = target - actual
        error = self.setpoint - self.measurement
        self.integral += (error * dT)
        derivative = (error - self.previous_error) / dT

        self.last_time = current_time

        return self.kP * error + self.kI * self.integral + self.kD * derivative