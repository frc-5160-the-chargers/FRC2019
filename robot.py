import magicbot
import wpilib
import wpilib.drive

import robotmap
import OI

import ctre

from components.drivetrain import Drivetrain

# flags
FBXC = True

class MyRobot(magicbot.MagicRobot):
    drivetrain : Drivetrain

    def createObjects(self):
        '''Create motors and stuff here'''
        # Launch vision services
        wpilib.CameraServer.launch('vision.py:main')

        self.rfMotor = ctre.WPI_TalonSRX(robotmap.frontRightDrive)
        self.rbMotor = ctre.WPI_TalonSRX(robotmap.backRightDrive)
        self.lbMotor = ctre.WPI_TalonSRX(robotmap.backLeftDrive)
        self.lfMotor = ctre.WPI_TalonSRX(robotmap.frontLeftDrive)

        self.leftMotors = wpilib.SpeedControllerGroup(self.lbMotor, self.lfMotor)
        self.rightMotors = wpilib.SpeedControllerGroup(self.rfMotor, self.rbMotor)
        
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
            self.drivetrain.handleDriving(wpilib.XboxController(0))
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.oi.twoStickMode = not self.oi.twoStickMode
        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)