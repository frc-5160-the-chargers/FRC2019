from wpilib import AnalogInput

class AnalogUltrasonicSensor:
    # these are the ones that use voltage
    volts_per_cm = 5/1024/10

    def __init__(self, port):
        self.port = port

    def getRawOutput(self):
        return AnalogInput.getVoltage(self.port)

    def getDistanceCm(self):
        return int(self.getRawOutput())*AnalogUltrasonicSensor.volts_per_cm