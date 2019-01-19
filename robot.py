import magicbot
import wpilib
import wpilib.drive

import robotmap
import OI
from OI import Side

import ctre

from components.drivetrain import Drivetrain

# flags
FBXC = True

class MyRobot(magicbot.MagicRobot):

    #High level components - list these first

    #Low level components
    drivetrain : Drivetrain

    def createObjects(self):
        '''Create motors and stuff here'''
        self.rfMotor = ctre.WPI_TalonSRX(robotmap.frontRightDrive)
        self.rbMotor = ctre.WPI_TalonSRX(robotmap.backRightDrive)
        self.lbMotor = ctre.WPI_TalonSRX(robotmap.backLeftDrive)
        self.lfMotor = ctre.WPI_TalonSRX(robotmap.frontLeftDrive)

        #configure motors - current limit, ramp rate, etc.

        self.rfMotor.configOpenLoopRamp(0.5)
        self.rbMotor.configOpenLoopRamp(0.5)
        self.lbMotor.configOpenLoopRamp(0.5)
        self.lfMotor.configOpenLoopRamp(0.5)

        #group motors
        self.leftMotors = wpilib.SpeedControllerGroup(self.lbMotor, self.lfMotor)
        self.rightMotors = wpilib.SpeedControllerGroup(self.rfMotor, self.rbMotor)
        
        #FBXC motors are oriented differently than on the newest chassis
        if FBXC:
            self.rightMotors.setInverted(True)
        else:
            self.leftMotors.setInverted(True)
        
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

        self.oi = OI.OI()

        

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass


    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        try:
            #this part does the wheels
            if self.oi.twoStickMode:
                self.drivetrain.driveRobot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)
            else:
                self.drivetrain.driveRobot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)

            #this part does the mode switching
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.oi.twoStickMode = not self.oi.twoStickMode


        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)