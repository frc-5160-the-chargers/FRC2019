import math

import magicbot
import wpilib
import wpilib.drive

import ctre

import robotmap
import OI
from OI import Side

from motorConfigurator import MotorConfigurator

from components.drivetrain import Drivetrain

class MyRobot(magicbot.MagicRobot):

    # High level components - list these first

    # Low level components
    drivetrain : Drivetrain

    def createObjects(self):
        """
        Create motors and stuff here
        """

        # drivetrain motors
        self.right_front_motor = ctre.WPI_TalonSRX(robotmap.right_front_drive)
        self.right_back_motor = ctre.WPI_TalonSRX(robotmap.right_back_drive)
        self.left_front_motor = ctre.WPI_TalonSRX(robotmap.left_front_drive)
        self.left_back_motor = ctre.WPI_TalonSRX(robotmap.left_back_drive)

        # configure motors - current limit, ramp rate, etc.
        MotorConfigurator.bulk_config_drivetrain(self.right_front_motor, self.right_back_motor, self.left_front_motor, self.left_back_motor)

        # create motor groups based on side
        self.left_drive_motors = wpilib.SpeedControllerGroup(self.left_back_motor, self.left_front_motor)
        self.right_drive_motors = wpilib.SpeedControllerGroup(self.right_front_motor, self.right_back_motor)

        # encoders
        self.left_encoder = wpilib.Encoder(aChannel=robotmap.left_encoder_a, bChannel=robotmap.left_encoder_b, reverseDirection=False, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.left_encoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)
        self.right_encoder = wpilib.Encoder(aChannel=robotmap.right_encoder_a, bChannel=robotmap.right_encoder_b, reverseDirection=False, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.right_encoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)

        # create drivetrain based on groupings
        self.drive = wpilib.drive.DifferentialDrive(self.left_drive_motors, self.right_drive_motors)

        # ahrs gyro
        self.gyro = wpilib.ADXRS450_Gyro(0)
        self.gyro.calibrate()

        # oi class
        self.oi = OI.OI()

        # launch automatic camera capturing for main drive cam
        # TODO Mount camera
        # wpilib.CameraServer.launch()

        self.driveLabels = ["dKP", "dKI", "dKD"]
        self.turnLabels = ["tKP", "tKI", "tKD"]

        for i in self.driveLabels:
            wpilib.SmartDashboard.putNumber(i, 0.1)
        for i in self.turnLabels:
            wpilib.SmartDashboard.putNumber(i, 0.1)



    def teleopInit(self):
        """
        Called when teleop starts; optional
        """
        self.gyro.reset()
        self.drivetrain.reset_encoders()

        # self.drivetrain.pid.set_setpoint_reset(self.drivetrain.TICKS_PER_INCH*12)
        # self.drivetrain.turn_to_position(90, timeout=5)


    def teleopPeriodic(self):
        """
        Called on each iteration of the control loop
        """
        try:
            # handle the drivetrain
            if self.oi.twoStickMode:
                self.drivetrain.teleop_drive_robot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)
            else:
                self.drivetrain.teleop_drive_robot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)

            # this part does the mode switching for driver control
            # TODO: move into OI
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.oi.twoStickMode = not self.oi.twoStickMode
                self.drivetrain.driver_takeover()

            # PID Testing is on the third controller
            # a: drive 3 feet
            # b: turn 90 degrees
            # x: read distance pid values
            # y: read turn pid values
            if wpilib.XboxController(2).getAButtonPressed():
                self.drivetrain.start_drive_to_position(12*3, timeout=20, tolerance=0.1, timeStable=3) # drive 3 feet or something
            
            if wpilib.XboxController(2).getBButtonPressed():
                self.drivetrain.start_turn_to_position(90) # turn 90 degrees
            
            if wpilib.XboxController(2).getXButtonPressed():
                self.drivetrain.drivePIDToleranceController.updateConstants(
                    kP=wpilib.SmartDashboard.getNumber(self.driveLabels[0], 0),
                    kI=wpilib.SmartDashboard.getNumber(self.driveLabels[1], 0),
                    kD=wpilib.SmartDashboard.getNumber(self.driveLabels[2], 0)
                )
                self.drivetrain.turnPIDToleranceController.updateConstants(
                    kP=wpilib.SmartDashboard.getNumber(self.turnLabels[0], 0),
                    kI=wpilib.SmartDashboard.getNumber(self.turnLabels[1], 0),
                    kD=wpilib.SmartDashboard.getNumber(self.turnLabels[2], 0)
                )
            if wpilib.XboxController(2).getBumperPressed(wpilib.XboxController.Hand.kRight):
                self.drivetrain.driver_takeover()

            print(self.gyro.getAngle())

        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)
