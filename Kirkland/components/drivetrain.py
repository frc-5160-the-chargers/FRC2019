import magicbot
import ctre
import wpilib
import wpilib.drive
from wpilib import DoubleSolenoid
from enum import Enum, unique, auto
from components.gearbox_shifter import GearboxShifter
from utils import PIDController, PIDToleranceController
from components import navx_handler

import robotmap

import time
import math

import OI

class DriveModes:
    TANKDRIVE = 0
    ARCADEDRIVE = 1
    PIDDISTANCE = 2
    PIDTURNING = 3

class Drivetrain:
    right_front_motor:  ctre.WPI_TalonSRX
    right_back_motor:   ctre.WPI_TalonSRX
    right_top_motor:    ctre.WPI_TalonSRX
    left_back_motor:    ctre.WPI_TalonSRX
    left_front_motor:   ctre.WPI_TalonSRX
    left_top_motor:     ctre.WPI_TalonSRX

    left_drive_motors: wpilib.SpeedControllerGroup
    right_drive_motors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    oi: OI.OI

    left_shifter : GearboxShifter
    right_shifter : GearboxShifter

    gyro : navx_handler.NavXHandler

    # configurable constants
    SHIFTDELAY = .5     # seconds between moving the shifter and restoring driver control
    SHIFTPOWER = .2    # power to use when shifting
    SHIFTTIMEOUT = 1    # time between shifting allowed
    REQUIRED_SHIFT_SPEED = 100

    def __init__(self):
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.square_inputs = False

        self.last_shift_time = 0
        self.shifting = False

        self.currentMode = DriveModes.TANKDRIVE

        self.drivePID = PIDController()
        self.drivePID.reset()
        self.drivePIDToleranceController = PIDToleranceController(self.drivePID, mi=-.75, ma=.75)

        self.turnPID = PIDController()
        self.turnPID.reset()
        self.turnPIDToleranceController = PIDToleranceController(self.turnPID, mi=-.5, ma=.5)

    def teleop_drive_robot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        if not self.shifting:
            self.left_motor_speed = left_motor_val
            self.right_motor_speed = right_motor_val
            self.square_inputs = square_inputs

    #get velocities of drivetrain encoders
    def get_right_velocity(self):
        return self.right_top_motor.getQuadratureVelocity()
    def get_left_velocity(self):
        return self.left_front_motor.getQuadratureVelocity()
    def get_average_velocity(self):
        return (self.get_right_velocity() + self.get_left_velocity()) / 2.0

    #get positions of drivetrain encoders
    def get_right_position(self):
        return self.right_top_motor.getQuadraturePosition()
    def get_left_position(self):
        return -self.left_front_motor.getQuadraturePosition()
    def get_average_position(self):
        return (self.get_right_position() + self.get_left_position()) / 2.0
    
    #reset either or both drive encoders
    def reset_left_encoder(self):
        self.right_top_motor.setQuadraturePosition(0)
    def reset_right_encoder(self):
        self.left_front_motor.setQuadraturePosition(0)
    def reset_encoders(self):
        self.reset_left_encoder()
        self.reset_right_encoder()

    def print_velocities(self):
        print("right side v: " + str(self.get_right_velocity()) + "left side v: " + str(self.get_left_velocity))

    def ready_to_shift(self):
        return abs(self.left_front_motor.getQuadratureVelocity()) > self.REQUIRED_SHIFT_SPEED

    def shift(self):
        """
        shift from current gear to other gear
            :param self: 
        """
        # first make sure that gearboxes are moving
        if self.ready_to_shift():
        # move solenoids
            self.left_shifter.toggle_shift()
            self.right_shifter.toggle_shift()

    def set_motor_powers(self):
        """
        set the power of the motors using the internal speeds
            :param self:
        """
        self.left_drive_motors.set(self.left_motor_speed)
        self.right_drive_motors.set(self.right_motor_speed)

    def stop_motors(self):
        """
        set both motor sets to be 0 power
            :param self: 
        """
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.set_motor_powers()

    def start_drive_to_position(self, distance, tolerance=1, timeout=5, timeStable=0.5):
        self.drivePIDToleranceController.start(distance, tolerance, timeout, timeStable)
        self.currentMode = DriveModes.PIDDISTANCE
        self.reset_encoders()

    def drive_to_position(self):
        kLeft = -1
        kRight = -1
        if not self.drivePIDToleranceController.isDone():
            pidOutput = self.drivePIDToleranceController.getOutput(self.get_average_position())
            self.drive.tankDrive(pidOutput*kLeft, pidOutput*kRight)
        else:
            self.drive.tankDrive(0, 0)

    def start_turn_to_position(self, degrees, tolerance=1, timeout=3, timeStable=0.5):
        self.turnPIDToleranceController.start(degrees, tolerance, timeout, timeStable)
        self.currentMode = DriveModes.PIDTURNING
        self.gyro.reset_rotation()

    def turn_to_position(self):
        # constants to apply to each motor side
        kLeft = 1
        kRight = -1
        if not self.turnPIDToleranceController.isDone():
            pidOutput = self.turnPIDToleranceController.getOutput(self.gyro.get_rotation())
            self.drive.tankDrive(pidOutput*kLeft, pidOutput*kRight)
        else:
            self.drive.tankDrive(0, 0)

    def driver_takeover(self):
        if self.oi.twoStickMode:
            self.currentMode = DriveModes.TANKDRIVE
        else:
            self.currentMode = DriveModes.ARCADEDRIVE

    def toggle_tankdrive(self):
        if self.currentMode in [DriveModes.TANKDRIVE, DriveModes.ARCADEDRIVE]:
            self.currentMode = DriveModes.TANKDRIVE if self.currentMode == DriveModes.ARCADEDRIVE else DriveModes.ARCADEDRIVE

    def execute(self):
        if self.currentMode == DriveModes.TANKDRIVE:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        if self.currentMode == DriveModes.ARCADEDRIVE:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        if self.currentMode == DriveModes.PIDDISTANCE:
            self.drive_to_position()
        if self.currentMode == DriveModes.PIDTURNING:
            self.turn_to_position()