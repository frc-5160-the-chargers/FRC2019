import math

import magicbot
import wpilib
import wpilib.drive

import navx

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
        self.left_encoder = wpilib.Encoder(aChannel=robotmap.left_encoder_a, bChannel=robotmap.left_encoder_b)
        self.left_encoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)
        self.left_encoder.setDistancePerPulse((robotmap.wheel_diameter*math.pi)/(256))
        self.right_encoder = wpilib.Encoder(aChannel=robotmap.right_encoder_a, bChannel=robotmap.right_encoder_b)
        self.right_encoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)
        self.left_encoder.setDistancePerPulse((robotmap.wheel_diameter*math.pi)/(256))

        # create drivetrain based on groupings
        self.drive = wpilib.drive.DifferentialDrive(self.left_drive_motors, self.right_drive_motors)

        # ahrs gyro
        self.gyro = wpilib.ADXRS450_Gyro(0)

        # oi class
        self.oi = OI.OI()

        # launch automatic camera capturing for main drive cam
        # TODO Mount camera
        # wpilib.CameraServer.launch()

        # PID tuning params on smartdashboard
        wpilib.SmartDashboard.putNumberArray("DriveForwardsPID", [0.2, 0, 0])
        wpilib.SmartDashboard.putNumberArray("TurnPID", [1, 0, 0])        


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
                self.drivetrain.start_drive_to_position(12*3) # drive 3 feet or something
            
            if wpilib.XboxController(2).getBButtonPressed():
                self.drivetrain.start_turn_to_position(90) # turn 90 degrees
            
            if wpilib.XboxController(2).getXButtonPressed():
                self.drivetrain.drivePid.kP, self.drivetrain.drivePid.kI, self.drivetrain.drivePid.kD = wpilib.SmartDashboard.getNumberArray("DriveForwardsPID", [0, 0, 0])
            
            if wpilib.XboxController(2).getYButtonPressed():
                self.drivetrain.turnPid.kP, self.drivetrain.turnPid.kI, self.drivetrain.turnPid.kD = wpilib.SmartDashboard.getNumberArray("TurnPID", [0,0,0])

            if wpilib.XboxController(2).getBumperPressed(wpilib.XboxController.Hand.kRight):
                self.drivetrain.driver_takeover()

        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)
