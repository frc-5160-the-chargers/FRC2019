import magicbot
import wpilib
import wpilib.drive

import robotmap
import OI
from OI import Side

import ctre

from components.drivetrain import Drivetrain
from components.hatch_extend import HatchExtend
from components.hatch_grab import HatchGrab
from components.hatch_mechanism import Hatch

# flags
FBXC = True

class MyRobot(magicbot.MagicRobot):

    #High level components - list these first
    hatch : Hatch
    #Low level components
    drivetrain : Drivetrain
    hatch_grab : HatchGrab
    hatch_extend : HatchExtend

    def createObjects(self):
        '''Create motors and stuff here'''

        #declare motors
        self.right_front_motor = ctre.WPI_TalonSRX(robotmap.front_right_drive)
        self.right_back_motor = ctre.WPI_TalonSRX(robotmap.back_right_drive)
        self.left_back_motor = ctre.WPI_TalonSRX(robotmap.back_left_drive)
        self.left_front_motor = ctre.WPI_TalonSRX(robotmap.front_left_drive)

        #declare pneumatic stuff
        self.hatch_extension_actuator = wpilib.DoubleSolenoid(0, 1)
        self.hatch_grab_actuator = wpilib.DoubleSolenoid(2, 3)

        #configure motors - current limit, ramp rate, etc.

        self.right_front_motor.configOpenLoopRamp(0.5)
        self.right_back_motor.configOpenLoopRamp(0.5)
        self.left_back_motor.configOpenLoopRamp(0.5)
        self.left_front_motor.configOpenLoopRamp(0.5)

        #group motors
        self.left_drive_motors = wpilib.SpeedControllerGroup(self.left_back_motor, self.left_front_motor)
        self.right_drive_motors = wpilib.SpeedControllerGroup(self.right_front_motor, self.right_back_motor)
        
        #FBXC motors are oriented differently than on the newest chassis
        if FBXC:
            self.right_drive_motors.setInverted(True)
        else:
            self.left_drive_motors.setInverted(True)
        
        self.drive = wpilib.drive.DifferentialDrive(self.left_drive_motors, self.right_drive_motors)

        self.oi = OI.OI()

        

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.oi.process_user_settings()


    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        try:
            #this part does the wheels
            if self.oi.twoStickMode:
                self.drivetrain.teleopDriveRobot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)
            else:
                self.drivetrain.teleopDriveRobot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)

            #operate the hatch mechanism
            #TODO this stuff
            #if self.oi.hatch_extend_control():
            #    self.

            #this part does the mode switching for driver control
            #TODO: Figure out how to make all references to the controller go into the OI
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.oi.twoStickMode = not self.oi.twoStickMode


        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)