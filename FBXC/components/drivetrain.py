import enum

from ctre import WPI_TalonSRX
from wpilib import SpeedControllerGroup, Encoder, ADXRS450_Gyro
from wpilib.drive import DifferentialDrive

import robotmap

from OI import OI, Side

class DriveModes(enum.Enum):
    DRIVEROPERATED = enum.auto()
    PIDOPERATED = enum.auto()

class Drivetrain:
    right_front_motor:  WPI_TalonSRX
    right_back_motor:   WPI_TalonSRX
    left_front_motor:   WPI_TalonSRX
    left_back_motor:    WPI_TalonSRX

    right_encoder: Encoder
    left_encoder: Encoder

    left_drive_motors: SpeedControllerGroup
    right_drive_motors: SpeedControllerGroup

    drive: DifferentialDrive

    oi: OI

    gyro: ADXRS450_Gyro

    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0

        self.speed = 0
        self.rotation = 0

        self.current_mode = DriveModes.DRIVEROPERATED

    def teleop_drive_robot(self, left_speed=0, right_speed=0, speed=0, rotation=0):
        self.left_speed = left_speed
        self.right_speed = right_speed
        self.speed = speed
        self.rotation = rotation

    #get positions of drivetrain encoders
    def get_right_position(self):
        return self.right_encoder.getDistance()
    def get_left_position(self):
        return -self.left_encoder.getDistance()
    def get_average_position(self):
        return ((self.get_right_position() + self.get_left_position()) / -2) * robotmap.inches_per_tick
    
    #reset either or both drive encoders
    def reset_left_encoder(self):
        self.left_encoder.reset()
    def reset_right_encoder(self):
        self.right_encoder.reset()
    def reset_encoders(self):
        self.reset_left_encoder()
        self.reset_right_encoder()

    def set_motor_powers(self):
        self.left_drive_motors.set(self.left_speed)
        self.right_drive_motors.set(self.right_speed)

    def reset_input(self):
        self.left_speed, self.right_speed, self.rotation, self.speed = (0, 0, 0, 0)

    def stop_motors(self):
        self.reset_input()
        self.set_motor_powers()

    def driver_takeover(self):
        self.current_mode = DriveModes.DRIVEROPERATED

    def execute(self):
        if self.current_mode == DriveModes.DRIVEROPERATED:
            if self.oi.arcade_drive:
                self.drive.arcadeDrive(self.speed, self.rotation)
            else:
                self.drive.tankDrive(self.left_speed, self.right_speed)

        if self.current_mode == DriveModes.PIDOPERATED:
            self.drive.arcadeDrive(self.speed, self.rotation)