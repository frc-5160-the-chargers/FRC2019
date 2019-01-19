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

    def driveRobot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        self.left_motor_speed = left_motor_val
        self.right_motor_speed = right_motor_val
        self.square_inputs = False

        self.twoStickMode = twoStick


    def execute(self):
        if self.twoStickMode:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        else:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)