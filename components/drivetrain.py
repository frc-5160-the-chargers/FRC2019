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
    right_front_motor: ctre.WPI_TalonSRX
    right_back_motor: ctre.WPI_TalonSRX
    left_back_motor: ctre.WPI_TalonSRX
    left_front_motor: ctre.WPI_TalonSRX

    left_drive_motors: wpilib.SpeedControllerGroup
    right_drive_motors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    oi: OI.OI

    left_shifter : GearboxShifter
    right_shifter : GearboxShifter

    # configurable constants
    SHIFTDELAY = .5     # seconds between moving the shifter and restoring driver control
    SHIFTPOWER = .1    # power to use when shifting
    SHIFTTIMEOUT = 1    # time between shifting allowed

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


    def shift(self):
        """
        shift from current gear to other gear
            :param self: 
        """
        # first make sure that time is ok for shifting
        if self.get_shift_time() < Drivetrain.SHIFTTIMEOUT:
            return
        
        # set flags
        self.shifting = True
        self.last_shift_time = time.time()

        # set motor power
        if self.oi.twoStickMode:
            self.left_motor_speed = math.copysign(Drivetrain.SHIFTPOWER, self.left_motor_speed)
            self.right_motor_speed = math.copysign(Drivetrain.SHIFTPOWER, self.right_motor_speed)
        else:
            self.left_motor_speed = math.copysign(Drivetrain.SHIFTPOWER, self.left_motor_speed)
            self.right_motor_speed = 0

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