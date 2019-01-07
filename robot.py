import magicbot
import wpilib

import ctre

from components.drivetrain import Drivetrain

class MyRobot(magicbot.MagicRobot):
    drivetrain : Drivetrain

    def createObjects(self):
        '''Create motors and stuff here'''
        self.testMotor = wpilib.Spark(0)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        try:
            self.drivetrain.setMotorPower(wpilib.XboxController(0).getX(0))
        except:
            self.onException()

if __name__ == '__main__':
    wpilib.run(MyRobot)