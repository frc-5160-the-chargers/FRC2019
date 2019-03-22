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

from controllers.drivetrain_pid import DriveStraightPID, TurnPID

class MyRobot(magicbot.MagicRobot):

    # High level components - list these first    
    controller_drive_straight : DriveStraightPID
    controller_turn :           TurnPID


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

        # pid controllers
        self.drive_forwards_pid = wpilib.PIDController(
                                    robotmap.drive_kP,
                                    robotmap.drive_kI, 
                                    robotmap.drive_kD,
                                    lambda: self.drivetrain.get_average_position(),
                                    lambda x: self.drivetrain.teleop_drive_robot(speed=x))
        self.turn_pid = wpilib.PIDController(
                                    robotmap.turn_kP,
                                    robotmap.turn_kI,
                                    robotmap.turn_kD,
                                    lambda: self.gyro.getAngle(),
                                    lambda x: self.drivetrain.teleop_drive_robot(rotation=x))




    def teleopInit(self):
        """
        Called when teleop starts; optional
        """
        self.gyro.reset()
        self.drivetrain.reset_encoders()
        self.oi.load_user_settings()

        # self.drivetrain.pid.set_setpoint_reset(self.drivetrain.TICKS_PER_INCH*12)
        # self.drivetrain.turn_to_position(90, timeout=5)


    def teleopPeriodic(self):
        """
        Called on each iteration of the control loop
        """
        try:
            # handle the drivetrain
            if self.oi.arcade_drive:
                self.drivetrain.teleop_drive_robot(speed=self.oi.process_driver_input(Side.LEFT), rotation=self.oi.process_driver_input(Side.RIGHT))
            else:
                self.drivetrain.teleop_drive_robot(left_speed=self.oi.process_driver_input(Side.LEFT), right_speed=self.oi.process_driver_input(Side.RIGHT))

            if self.oi.arcade_tank_shift():
                self.oi.arcade_drive = not self.oi.arcade_drive

            if self.oi.beast_mode():
                self.controller_drive_straight.drive_distance(500)

        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)
