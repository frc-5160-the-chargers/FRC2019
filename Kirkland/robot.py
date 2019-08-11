# robot.py
# the actual robot code and main execution stuff

import magicbot
import wpilib
import ctre

import networktables

from components.cargo_mechanism import *
from components.drivetrain import *
from components.hatch_mechanism import *
from components.pressure_sensor import *

import robotmap
from oi import OI


class Robot(magicbot.MagicRobot):
    # high level components
    cargo_mechanism: CargoMechanism
    hatch_mechanism: HatchMechanism
    drivetrain_mechanism: DrivetrainMechanism
    pressure_sensor: PressureSensor

    # low level components
    cargo_rotator: CargoRotator
    cargo_locking_servo: CargoServo

    hatch_grabber: HatchGrabber
    hatch_rack: HatchRack

    drivetrain: Drivetrain
    shifters: Shifters

    def createObjects(self):
        # CARGO MECHANISM
        self.cargo_mechanism_motor_rotator = ctre.WPI_TalonSRX(
            robotmap.Ports.Cargo.rotator)
        self.cargo_mechanism_servo_lock = wpilib.Servo(
            robotmap.Ports.Cargo.locking_servo)

        utils.configure_motor(
            self.cargo_mechanism_motor_rotator, ctre.NeutralMode.Brake)

        # HATCH MECHANISM
        self.hatch_grab_actuator = wpilib.DoubleSolenoid(
            robotmap.Ports.Hatch.Grabber.pcm, robotmap.Ports.Hatch.Grabber.front, robotmap.Ports.Hatch.Grabber.back)
        self.hatch_rack_actuator_left = wpilib.DoubleSolenoid(
            robotmap.Ports.Hatch.Extension.pcm, robotmap.Ports.Hatch.Extension.left_front, robotmap.Ports.Hatch.Extension.left_back)
        self.hatch_rack_actuator_right = wpilib.DoubleSolenoid(
            robotmap.Ports.Hatch.Extension.pcm, robotmap.Ports.Hatch.Extension.right_front, robotmap.Ports.Hatch.Extension.right_back)

        # DRIVETRAIN SYSTEM
        # TODO fix motor port naming.
        self.drivetrain_right_front = ctre.WPI_TalonSRX(
            robotmap.Ports.Drivetrain.Motors.right_back)
        self.drivetrain_right_back = ctre.WPI_TalonSRX(
            robotmap.Ports.Drivetrain.Motors.right_bottom)
        self.drivetrain_right_top = ctre.WPI_TalonSRX(
            robotmap.Ports.Drivetrain.Motors.right_top)

        self.drivetrain_left_front = ctre.WPI_TalonSRX(
            robotmap.Ports.Drivetrain.Motors.left_front)
        self.drivetrain_left_back = ctre.WPI_TalonSRX(
            robotmap.Ports.Drivetrain.Motors.left_bottom)
        self.drivetrain_left_top = ctre.WPI_TalonSRX(
            robotmap.Ports.Drivetrain.Motors.left_top)

        utils.configure_drivetrain_motors(self.drivetrain_left_back, self.drivetrain_left_front, self.drivetrain_left_top,
                                          self.drivetrain_right_back, self.drivetrain_right_front, self.drivetrain_right_top)

        self.drivetrain_right_motors = wpilib.SpeedControllerGroup(
            self.drivetrain_right_back, self.drivetrain_right_front, self.drivetrain_right_top)
        self.drivetrain_left_motors = wpilib.SpeedControllerGroup(
            self.drivetrain_left_back, self.drivetrain_left_front, self.drivetrain_left_top)

        self.differential_drive = wpilib.drive.DifferentialDrive(
            self.drivetrain_left_motors, self.drivetrain_right_motors)

        self.left_shifter_actuator = wpilib.DoubleSolenoid(
            robotmap.Ports.Drivetrain.Shifters.pcm, robotmap.Ports.Drivetrain.Shifters.left_front, robotmap.Ports.Drivetrain.Shifters.left_back)
        self.right_shifter_actuator = wpilib.DoubleSolenoid(
            robotmap.Ports.Drivetrain.Shifters.pcm, robotmap.Ports.Drivetrain.Shifters.right_front, robotmap.Ports.Drivetrain.Shifters.right_back)

        self.pressure_sensor_input = wpilib.AnalogInput(
            robotmap.Ports.PressureSensor.port)

        # MISC
        self.oi = OI()

        # run camera streaming program
        wpilib.CameraServer.launch("camera_streaming.py:main")
        self.current_camera = 0
        self.camera_table = networktables.NetworkTables.getTable("/CameraPublisher")

        # this is important for this year...
        self.use_teleop_in_autonomous = True

    def teleopInit(self):
        self.drivetrain_mechanism.reset()
        self.cargo_mechanism.reset()
        self.hatch_mechanism.reset()

    def teleopPeriodic(self):
        with self.consumeExceptions():
            pass
        
if __name__ == "__main__":
    wpilib.run(Robot)