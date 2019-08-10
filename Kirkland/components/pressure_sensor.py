from wpilib import AnalogInput

from Kirkland import robotmap


class PressureSensor:
    pressure_sensor_input: AnalogInput

    def __init__(self):
        self.normalized_voltage = 1.606

    def get_raw_output(self):
        return self.pressure_sensor_input.getVoltage()

    def get_uncalibrated_pressure(self):
        # NOTE this assumes that Vcc is 5.0V
        return 250 * (self.get_raw_output() / 5.0) - 25

    def get_pressure(self):
        return 250 * (self.get_raw_output() / self.normalized_voltage) - 25

    def calibrate_pressure(self):
        # call this function when the air tanks are at 110 psi or their max pressure to calibrate
        self.normalized_voltage = (self.get_raw_output(
        ) * 250) / (robotmap.Physics.PressureSensor.calibration_pressure + 25)

    def execute(self):
        pass