import magicbot
import ctre
import wpilib
import wpilib.drive
from wpilib import DoubleSolenoid
from enum import Enum, unique, auto
from components.gearbox_shifter import GearboxShifter
from utils import PIDController

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
        return (self.get_right_position() + self.get_left_position) / 2.0
    
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
    
    def drive_set_distance(self, distance):
        #distance measured in encoder ticks
        measurement = self.get_average_position()
        pid = PIDController(measurement)
        pid.set_setpoint(distance)
        self.drive.tankDrive(pid.pID())

    def execute(self):
        if self.oi.twoStickMode:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        else:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        
        if self.oi.drivetrain_shifting_control():
            self.shift()

        #I don't think this has to exist but it might so I commented it out
        self.left_shifter.execute()
        self.right_shifter.execute()