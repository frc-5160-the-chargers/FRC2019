import time

class PIDController:

    def __init__(self, kP=1, kI=0, kD=0):
        """
        constructor
            :param self: 
            :param kP=1: kP value to use for this controller, default is 1
            :param kI=0: kI value, defualts to 0 (not in use)
            :param kD=0: kD value, defaults to 0 (not in use)
        """
        self.setpoint = 0
        self.measurement = 0

        self.kP = kP
        self.kI = kI
        self.kD = kD

        self.integral = 0
        self.previous_error = 0
        self.last_time = 0

    def reset(self):
        """
        reset the pid controller for reuse
            :param self: 
        """
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()

    def set_setpoint_reset(self, setpoint):
        """
        set the setpoint of this pid controller and reset for reuse
            :param self: 
            :param setpoint: the setpoint of the controller
        """
        self.setpoint = setpoint
        self.reset()

    def pid(self, measurement):
        """
        calculate the output given the input measurement. should be called as frequently as possible while in use
            :param self: 
            :param meausrement: last reading from whatever is being used to make the measurementdef pid(self, meausrement)
        """
        self.measurement = measurement

        # calculate time in ms since last called
        current_time = time.time()
        dT = current_time - self.last_time

        # error = target - actual
        error = self.setpoint - self.measurement
        self.integral += (error * dT)
        derivative = (error - self.previous_error) / dT

        self.last_time = current_time

        a = self.kP * error + self.kI * self.integral + self.kD * derivative
        return a