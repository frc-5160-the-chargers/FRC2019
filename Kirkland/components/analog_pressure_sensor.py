from wpilib import AnalogInput

class AnalogPressureSensor():

    #pressure to charge pneumatics to for calibration
    #TODO figure out the pressure that the switch stops at
    CALIBRATION_PRESSURE = 110

    def __init__(self, port):
        self.port = port
    
    def get_raw_output(self):
        return AnalogInput.getVoltage(self.port)

    def get_uncalibrated_pressure_psi(self):
        """return pressure without calibrating (assuming Vcc is 5.0V)"""
        return 250 * (AnalogInput.getVoltage(self.port) / 5.0) - 25

    def get_pressure_psi(self):
        """return calibrated pressure (take Vcc variability into account)"""
        return 250 * (AnalogInput.getVoltage(self.port) / self.normalized_voltage) - 25
    
    def calibrate_pressure(self):
        """calibrate the sensor to account for Vcc variability"""

        """
        CALIBRATION STEPS:
        1. Charge air tanks to 110 psi (or whatever the compressor stops at)
        2. press calibration button (TBD)     
        """

        self.normalized_voltage = float(AnalogInput.getVoltage(self.port) / ((0.004 * self.CALIBRATION_PRESSURE) + 0.1))