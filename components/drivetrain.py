import magicbot
import ctre
import wpilib
import wpilib.drive
import OI

class Drivetrain:
    right_front_motor: ctre.WPI_TalonSRX
    right_back_motor: ctre.WPI_TalonSRX
    left_back_motor: ctre.WPI_TalonSRX
    left_front_motor: ctre.WPI_TalonSRX
    
    left_drive_motors: wpilib.SpeedControllerGroup
    right_drive_motors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    oi: OI.OI

    def teleopDriveRobot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        self.left_motor_speed = left_motor_val
        self.right_motor_speed = right_motor_val
        self.square_inputs = False

        self.twoStickMode = twoStick


    def execute(self):
        if self.twoStickMode:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        else:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)