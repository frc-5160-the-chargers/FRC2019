from wpilib import AnalogInput

class AnalogUltrasonicSensor:
    # these are the ones that use voltage

    def __init__(self, port):
        self.port = port

    def getRawOutput(self):
        return AnalogInput.getVoltage(self.port)

    def getDistanceCm(self):
        return int(self.getRawOutput())/2