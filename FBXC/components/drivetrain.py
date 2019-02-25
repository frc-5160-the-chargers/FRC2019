import magicbot
import ctre
import wpilib
import wpilib.drive
from wpilib import DoubleSolenoid
from enum import Enum, unique, auto
from utils import PIDController, PIDToleranceController

import time
import math

import OI

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

        self.drivePid = PIDController(kP=0.0002)
        self.drivePid.reset()
        
        self.turnPid = PIDController(kP=1)
        self.turnPid.reset()

    def teleop_drive_robot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        self.left_motor_speed = left_motor_val
        self.right_motor_speed = right_motor_val
        self.square_inputs = square_inputs

    #get positions of drivetrain encoders
    def get_right_position(self):
        return self.right_encoder.getDistance()
    def get_left_position(self):
        return self.left_encoder.getDistance()
    def get_average_position(self):
        return (self.get_right_position() + self.get_left_position()) / 2.0
    
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

    def drive_to_position(self, distance, tolerance=1, timeout=5, timeStable=0.5):
        """
        very similar parameters to turn_to_position TODO write this doc out later
        """
        self.drivePid.set_setpoint_reset(distance)
        kLeft = 1
        kRight = 1
        error = tolerance+1
        startTime = time.time()
        lastTimeNotInTolerance = startTime
        self.reset_encoders()
        while time.time() < timeout+startTime:
            pidOutput = self.drivePid.pid(self.get_average_position())
            self.left_motor_speed = pidOutput*kLeft
            self.right_motor_speed = pidOutput*kRight
            self.set_motor_powers()
            if abs(error) > tolerance:                              # not in tolerance
                lastTimeNotInTolerance = time.time()
            if time.time()-lastTimeNotInTolerance > timeStable:     # has been in tolerance long enough
                self.stop_motors()
                return True
        self.stop_motors()
        return False

    def turn_to_position(self, degrees, tolerance=1, timeout=3, timeStable=0.5):
        """
        turn to a given position (degrees) using PID
            :param self: 
            :param degrees: the position to turn to
            :param tolerance=1: the tolerance (in degrees)
            :param timeout=3: the timeout (in seconds) or length to run until its done
            :param timeStable=0.5: the number of seconds to keep the error within the tolerance before ending
            :returns: True if done because error is within tolerance otherwise False
        """
        # TODO: Tune these values and integrate with PID class
        self.turnPid.set_setpoint_reset(degrees)
        # constants to apply to each motor side
        kLeft = -0.5
        kRight = -0.5
        error = tolerance+1
        startTime = time.time()
        lastTimeNotInTolerance = time.time()
        self.gyro.reset()
        while time.time() < startTime+timeout:
            pidOutput = self.turnPid.pid(self.gyro.getAngle())
            self.left_motor_speed = pidOutput*kLeft
            self.right_motor_speed = pidOutput*kRight
            self.set_motor_powers()
            if abs(error) > tolerance:
                lastTimeNotInTolerance = time.time()
            if time.time()-lastTimeNotInTolerance > timeStable:
                self.stop_motors()
                return True
        self.stop_motors()
        return False

    def execute(self):
        if self.oi.twoStickMode:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        else:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)