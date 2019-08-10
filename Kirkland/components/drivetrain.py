# drivetrain.py
# the code to control the drivetrain and shifters

from ctre import WPI_TalonSRX
from wpilib import SpeedControllerGroup, DoubleSolenoid
from wpilib.drive import DifferentialDrive

from Kirkland import robotmap

import enum
import utils


class ShifterGear(enum.Enum):
    LOW_GEAR = enum.auto()
    HIGH_GEAR = enum.auto()


class Shifters:
    left_shifter_actuator: DoubleSolenoid
    right_shifter_actuator: DoubleSolenoid

    def __init__(self):
        # NOTE: make sure that the robot is forced into low gear at the start of a match
        self.gear = ShifterGear.LOW_GEAR

    def shift_up(self):
        self.gear = ShifterGear.HIGH_GEAR

    def shift_down(self):
        self.gear = ShifterGear.LOW_GEAR

    def toggle(self):
        self.gear = ShifterGear.LOW_GEAR if self.gear == ShifterGear.HIGH_GEAR else ShifterGear.HIGH_GEAR

    def execute(self):
        if self.gear == ShifterGear.LOW_GEAR:
            self.left_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.low_gear_state)
            self.right_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.low_gear_state)

        if self.gear == ShifterGear.HIGH_GEAR:
            self.left_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.high_gear_state)
            self.right_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.high_gear_state)


class DriveModes(enum.Enum):
    TANKDRIVE = enum.auto()
    ARCADEDRIVE = enum.auto()


class Drivetrain:
    drivetrain_right_front: WPI_TalonSRX
    drivetrain_right_back: WPI_TalonSRX
    drivetrain_right_top: WPI_TalonSRX

    drivetrain_left_front: WPI_TalonSRX
    drivetrain_left_back: WPI_TalonSRX
    drivetrain_left_top: WPI_TalonSRX

    drivetrain_left_motors: SpeedControllerGroup
    drivetrain_right_motors: SpeedControllerGroup

    differential_drive: DifferentialDrive

    def __init__(self):
        self.drive_mode = DriveModes.ARCADEDRIVE

        self.left_power = 0
        self.right_power = 0

        self.speed = 0
        self.rotation = 0

    def arcade_drive(self, power, rotation):
        self.drive_mode = DriveModes.ARCADEDRIVE
        self.speed = power
        self.rotation = rotation

    def tank_drive(self, left_power, right_power):
        self.drive_mode = DriveModes.TANKDRIVE
        self.left_power = left_power
        self.right_power = right_power

    def stop_motors(self):
        self.left_power = 0
        self.right_power = 0

        self.speed = 0
        self.rotation = 0

        self.differential_drive.stopMotor()

    def get_left_position(self):
        # NOTE: left_front is the one with the left encoder
        return -self.drivetrain_left_front.getQuadraturePosition() / robotmap.Physics.Drivetrain.Encoders.ticks_per_inch

    def get_left_velocity(self):
        return -self.drivetrain_left_front.getQuadratureVelocity()

    def get_right_position(self):
        # NOTE: right_front has the right encoder
        return self.drivetrain_right_top.getQuadraturePosition() / robotmap.Physics.Drivetrain.Encoders.ticks_per_inch

    def get_right_velocity(self):
        return self.drivetrain_right_top.getQuadratureVelocity()

    def get_average_position(self):
        return (self.get_left_position() + self.get_right_position()) / 2

    def get_average_velocity(self):
        return (self.get_left_velocity() + self.get_right_velocity()) / 2

    def reset_encoders(self):
        self.drivetrain_left_front.setQuadraturePosition(0)
        self.drivetrain_right_top.setQuadraturePosition(0)

    def execute(self):
        if self.drive_mode == DriveModes.TANKDRIVE:
            self.differential_drive.tankDrive(
                self.left_power, self.right_power)
        if self.drive_mode == DriveModes.ARCADEDRIVE:
            self.differential_drive.arcadeDrive(self.speed, self.rotation)


class DrivetrainMechanism:
    drivetrain: Drivetrain
    shifters: Shifters

    def __init__(self):
        pass

    def shift_up(self):
        if robotmap.Tuning.Drivetrain.shifting_speed_enabled:
            if abs(self.drivetrain.get_average_velocity()) > robotmap.Tuning.Drivetrain.min_shifting_speed:
                self.shifters.shift_up()
        else:
            self.shifters.shift_up()

    def shift_down(self):
        if robotmap.Tuning.Drivetrain.shifting_speed_enabled:
            if abs(self.drivetrain.get_average_velocity()) > robotmap.Tuning.Drivetrain.min_shifting_speed:
                self.shifters.shift_down()
        else:
            self.shifters.shift_down()

    def execute(self):
        pass
