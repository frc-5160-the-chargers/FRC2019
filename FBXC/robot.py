import math

import magicbot
import wpilib
import wpilib.drive

import ctre

from components.arduino import ArduinoHandler

from arduino.data_server import ArduinoServer

import robotmap
import OI
from OI import Side

from motorConfigurator import MotorConfigurator

from components.drivetrain import Drivetrain, DriveModes

from controllers.alignment_routine import AlignmentController

class MyRobot(magicbot.MagicRobot):

    # High level components - list these first
    controller_alignment :      AlignmentController



    # Low level components
    drivetrain : Drivetrain
    arduino_component : ArduinoHandler


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
        wpilib.CameraServer.launch()

        # launch arduino code and start data server
        self.arduino_server = ArduinoServer()
        self.arduino_server.startServer()


    def teleopInit(self):
        """
        Called when teleop starts; optional
        """
        self.gyro.reset()
        self.drivetrain.reset_encoders()
        self.oi.load_user_settings()

        self.controller_alignment.stop_reset_drivetrain()


        # self.drivetrain.pid.set_setpoint_reset(self.drivetrain.TICKS_PER_INCH*12)
        # self.drivetrain.turn_to_position(90, timeout=5)

    def teleopPeriodic(self):
        """
        Called on each iteration of the control loop
        """
        try:
            # handle the drivetrain
            if self.drivetrain.current_mode == DriveModes.DRIVEROPERATED:
                if self.oi.arcade_drive:
                    self.drivetrain.teleop_drive_robot(speed=self.oi.process_driver_input(Side.LEFT), rotation=self.oi.process_driver_input(Side.RIGHT))
                else:
                    self.drivetrain.teleop_drive_robot(left_speed=self.oi.process_driver_input(Side.LEFT), right_speed=self.oi.process_driver_input(Side.RIGHT))

            if self.oi.arcade_tank_shift():
                self.oi.arcade_drive = not self.oi.arcade_drive
            
            # do pid testing routines if button is pressed
            # drive 36 inches
            if wpilib.XboxController(0).getAButtonPressed():
                self.controller_alignment.start_alignment()
            
            # turn 90 degrees
            if wpilib.XboxController(0).getBButtonPressed():
                self.controller_alignment.interrupt()

            wpilib.SmartDashboard.putString("PixyCam Status", "Line Detected" if self.arduino_component.safe_to_detect() else "Line not detected")
        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)
