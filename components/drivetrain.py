import magicbot
import ctre
import wpilib
import wpilib.drive
from wpilib import DoubleSolenoid
from enum import Enum, unique, auto
from components.gearbox_shifter import GearboxShifter

import time
import math

import OI

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

    def teleop_drive_robot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        if not self.shifting:
            self.left_motor_speed = left_motor_val
            self.right_motor_speed = right_motor_val
            self.square_inputs = square_inputs

    def get_shift_time(self):
        """
        see what the time delta is from the last shifting operation
            :param self: 
        """
        return time.time() - self.last_shift_time

    def print_velocities(self):
        print("right side v: " + str(self.right_front_motor.getQuadratureVelocity()) + "left side v: " + str(self.left_front_motor.getQuadratureVelocity()))

    def ready_to_shift(self):
        return abs(self.left_front_motor.getQuadratureVelocity()) > self.REQUIRED_SHIFT_SPEED

    def shift(self):
        """
        shift from current gear to other gear
            :param self: 
        """
        # first make sure that time is ok for shifting
        if self.ready_to_shift():
        # move solenoids
            self.left_shifter.toggle_shift()
            self.right_shifter.toggle_shift()
        

    def execute(self):
        if self.oi.twoStickMode:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        else:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        
        if self.shifting:
            shift_delta = self.get_shift_time()
            if shift_delta > Drivetrain.SHIFTDELAY:
                self.shifting = False

        self.left_shifter.execute()
        self.right_shifter.execute()