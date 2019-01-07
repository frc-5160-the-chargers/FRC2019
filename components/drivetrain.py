import magicbot
import ctre
import wpilib
import wpilib.drive

class Drivetrain:
    rfMotor: ctre.WPI_TalonSRX
    rbMotor: ctre.WPI_TalonSRX
    lbMotor: ctre.WPI_TalonSRX
    lfMotor: ctre.WPI_TalonSRX
    
    leftMotors: wpilib.SpeedControllerGroup
    rightMotors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    def execute(self):
        pass

    def handleDriving(self, joystick : wpilib.XboxController):
        self.drive.arcadeDrive(joystick.getY(wpilib.XboxController.Hand.kLeft), joystick.getX(wpilib.XboxController.Hand.kLeft))