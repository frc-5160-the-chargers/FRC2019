import magicbot
import ctre
import wpilib
import wpilib.drive
from wpilib import DoubleSolenoid
from enum import Enum, unique, auto
from utils import PIDController, PIDToleranceController
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
    left_front_motor:   ctre.WPI_TalonSRX
    left_back_motor:    ctre.WPI_TalonSRX

    right_encoder: wpilib.Encoder
    left_encoder: wpilib.Encoder

    left_drive_motors: wpilib.SpeedControllerGroup
    right_drive_motors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    oi: OI.OI

    gyro: wpilib.ADXRS450_Gyro

    def __init__(self):
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.square_inputs = False

        self.currentMode = DriveModes.TANKDRIVE

        self.drivePid = PIDController(kP=0.75*0.9, kI=0.75*0.54/10, kD=0.3)
        self.drivePid.reset()
        self.drivePIDToleranceController = PIDToleranceController(self.drivePid, mi=-0.75, ma=0.75)
        
        self.turnPid = PIDController(kP=1)
        self.turnPid.reset()
        self.turnPIDToleranceController = PIDToleranceController(self.turnPid, mi=-.5, ma=.5)

    def teleop_drive_robot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        self.left_motor_speed = left_motor_val
        self.right_motor_speed = right_motor_val
        self.square_inputs = square_inputs

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
        self.gyro.reset()

    def turn_to_position(self):
        # constants to apply to each motor side
        kLeft = 1
        kRight = -1
        if not self.turnPIDToleranceController.isDone():
            pidOutput = self.turnPIDToleranceController.getOutput(self.gyro.getAngle())
            self.drive.tankDrive(pidOutput*kLeft, pidOutput*kRight)
        else:
            self.drive.tankDrive(0, 0)

    def driver_takeover(self):
        if self.oi.twoStickMode:
            self.currentMode = DriveModes.TANKDRIVE
        else:
            self.currentMode = DriveModes.ARCADEDRIVE

    def execute(self):
        if self.currentMode == DriveModes.TANKDRIVE:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        if self.currentMode == DriveModes.ARCADEDRIVE:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        if self.currentMode == DriveModes.PIDDISTANCE:
            self.drive_to_position()
        if self.currentMode == DriveModes.PIDTURNING:
            self.turn_to_position()