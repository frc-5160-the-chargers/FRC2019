import magicbot
import ctre
import wpilib
import wpilib.drive
from wpilib import DoubleSolenoid
from enum import Enum, unique, auto

import OI

class Drivetrain:
    right_front_motor: ctre.WPI_TalonSRX
    right_back_motor: ctre.WPI_TalonSRX
    left_back_motor: ctre.WPI_TalonSRX
    left_front_motor: ctre.WPI_TalonSRX

    left_shifter : wpilib.DoubleSolenoid
    right_shifter : wpilib.DoubleSolenoid
    
    left_drive_motors: wpilib.SpeedControllerGroup
    right_drive_motors: wpilib.SpeedControllerGroup

    drive: wpilib.drive.DifferentialDrive

    oi: OI.OI

    def __init__(self):
        self.high_gear = True
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.square_inputs = False

    def shift(self):
        self.high_gear = not self.high_gear
    
    def get_drivetrain_gear(self):
        return self.high_gear

    def teleop_drive_robot(self, twoStick, left_motor_val=0, right_motor_val=0, square_inputs=False):
        self.left_motor_speed = left_motor_val
        self.right_motor_speed = right_motor_val
        self.square_inputs = square_inputs
        self.twoStickMode = twoStick

    def execute(self):
        if self.twoStickMode:
            self.drive.tankDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        else:
            self.drive.arcadeDrive(self.left_motor_speed, self.right_motor_speed, self.square_inputs)
        
        #actuate shifters
        if self.high_gear:
            self.left_shifter.set(DoubleSolenoid.Value.kReverse)
            self.right_shifter.set(DoubleSolenoid.Value.kReverse)
        elif not self.high_gear:
            self.left_shifter.set(DoubleSolenoid.Value.kForward)
            self.right_shifter.set(DoubleSolenoid.Value.kForward)