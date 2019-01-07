import magicbot
import ctre
import wpilib

class Drivetrain:
    testMotor: wpilib.Spark
    drive: wpilib.drive.DifferentialDrive

    def execute(self):
        pass

    def setMotorPower(self, i):
        self.testMotor.set(i)