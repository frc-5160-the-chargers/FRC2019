import magicbot
import wpilib
import wpilib.drive

import robotmap

import ctre

from components.drivetrain import Drivetrain

class MyRobot(magicbot.MagicRobot):
    drivetrain : Drivetrain

    def createObjects(self):
        # Launch vision services
        wpilib.CameraServer.launch('vision.py:main')

        '''Create motors and stuff here'''
        self.rfMotor = ctre.WPI_TalonSRX(robotmap.frontRightDrive)
        self.rbMotor = ctre.WPI_TalonSRX(robotmap.backRightDrive)
        self.lbMotor = ctre.WPI_TalonSRX(robotmap.backLeftDrive)
        self.lfMotor = ctre.WPI_TalonSRX(robotmap.frontLeftDrive)

        self.leftMotors = wpilib.SpeedControllerGroup(self.lbMotor, self.lfMotor)
        self.rightMotors = wpilib.SpeedControllerGroup(self.rfMotor, self.rbMotor)
        self.rightMotors.setInverted(True)
        
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass


    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        try:
            self.drivetrain.handleDriving(wpilib.XboxController(0))
        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)