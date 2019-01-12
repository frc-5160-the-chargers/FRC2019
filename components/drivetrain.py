import magicbot
import ctre
import wpilib
import wpilib.drive
import OI

class Drivetrain:
    rfMotor: ctre.WPI_TalonSRX
    rbMotor: ctre.WPI_TalonSRX
    lbMotor: ctre.WPI_TalonSRX
    lfMotor: ctre.WPI_TalonSRX
    
    leftMotors: wpilib.SpeedControllerGroup
    rightMotors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    oi: OI.OI

    def execute(self):
        pass

    def handleDriving(self, joystick : wpilib.XboxController):
        if self.oi.twoStickMode:
            self.drive.tankDrive(self.oi.process(joystick.getRawAxis(5 if self.oi.beastMode else 1)), self.oi.process(joystick.getRawAxis(1 if self.oi.beastMode else 5)))
        else:
            self.drive.arcadeDrive(self.oi.process(joystick.getRawAxis(1)), -joystick.getRawAxis(4)/2)