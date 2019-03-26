import enum

from ctre import WPI_TalonSRX
from wpilib import SpeedControllerGroup
from wpilib.drive import DifferentialDrive

import robotmap

from oi import OI, Side

import utils

class DriveModes(enum.Enum):
    DRIVEROPERATED = enum.auto()
    PIDOPERATED = enum.auto()
    ALIGNMENTOPERATED = enum.auto()

class Drivetrain:
    right_front_motor:  WPI_TalonSRX
    right_back_motor:   WPI_TalonSRX
    right_top_motor:    WPI_TalonSRX
    left_back_motor:    WPI_TalonSRX
    left_front_motor:   WPI_TalonSRX
    left_top_motor:     WPI_TalonSRX

    left_drive_motors:  SpeedControllerGroup
    right_drive_motors: SpeedControllerGroup

    drive:              DifferentialDrive

    oi:                 OI

    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0

        self.speed = 0
        self.rotation = 0

        self.current_mode = DriveModes.DRIVEROPERATED

        self.drive_power_align_constant = robotmap.drive_power_constant

    def teleop_drive_robot(self, left_speed=0, right_speed=0, speed=0, rotation=0):
        self.left_speed = left_speed
        self.right_speed = right_speed
        self.speed = speed
        self.rotation = rotation

    def get_left_position(self):
        # NOTE left_front_motor has the left encoder
        return -self.left_front_motor.getQuadraturePosition() / robotmap.ticks_per_inch
    def get_right_position(self):
        # NOTE right_top_motor has the right encoder
        return self.right_top_motor.getQuadraturePosition() / robotmap.ticks_per_inch
    def get_average_position(self):
        return (self.get_left_position()+self.get_right_position()) / 2.0

    def get_left_velocity(self):
        return self.left_front_motor.getQuadratureVelocity()
    def get_right_velocity(self):
        return self.right_top_motor.getQuadratureVelocity()
    def get_average_velocity(self):
        return (self.get_left_velocity+self.get_right_velocity) / 2.0

    def reset_left_encoder(self):
        self.left_front_motor.setQuadraturePosition(0)
    def reset_right_encoder(self):
        self.right_top_motor.setQuadraturePosition(0)
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
            # NOTE when doing pid driving it is usually a good idea to limit the speed a bit 
            self.speed = utils.clamp(self.speed, -robotmap.drive_pid_power_straight, robotmap.drive_pid_power_straight)
            self.rotation = utils.clamp(self.rotation, -robotmap.drive_pid_power_turn, robotmap.drive_pid_power_turn)
            self.drive.arcadeDrive(self.speed, self.rotation)

        if self.current_mode == DriveModes.ALIGNMENTOPERATED:
            self.left_speed = utils.clamp(self.left_speed, -robotmap.drive_pid_power_turn, robotmap.drive_pid_power_turn)
            self.right_speed = utils.clamp(self.right_speed, -robotmap.drive_pid_power_turn, robotmap.drive_pid_power_turn)
            self.drive.tankDrive(self.left_speed, self.right_speed)