# robot.py
# the actual robot code and main execution stuff

import magicbot
import wpilib
from wpilib import SmartDashboard as dash
import ctre
import navx

import networktables

from components.cargo_mechanism import *
from components.drivetrain import *
from components.hatch_mechanism import *
from components.pressure_sensor import *

import robotmap
from oi import OI


class MyRobot(magicbot.MagicRobot):
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
        wpilib.CameraServer.launch("vision.py:main")
        self.current_camera = 0
        self.camera_table = networktables.NetworkTables.getTable(
           "/CameraPublisher")

        # this is important for this year...
        self.use_teleop_in_autonomous = True

        self.navx = navx.AHRS.create_spi()

    def teleopInit(self):
        self.drivetrain_mechanism.reset()
        self.cargo_mechanism.reset()
        self.hatch_mechanism.reset()

    def teleopPeriodic(self):
        try:
            # DRIVETRAIN
            if self.drivetrain.drive_mode == DriveModes.ARCADEDRIVE:
                self.drivetrain.arcade_drive(self.oi.drivetrain_curve(self.oi.driver.getY(
                    self.oi.driver.Hand.kLeft)), -self.oi.driver.getX(self.oi.driver.Hand.kRight)/1.5)
            elif self.drivetrain.drive_mode == DriveModes.TANKDRIVE:
                self.drivetrain.tank_drive(self.oi.drivetrain_curve(self.oi.driver.getY(
                    self.oi.driver.Hand.kLeft)), self.oi.drivetrain_curve(self.oi.driver.getY(self.oi.driver.Hand.kRight)))
            elif self.drivetrain.drive_mode == DriveModes.DRIVESTRAIGHTARCADE:
                self.drivetrain.drive_straight(self.oi.drivetrain_curve(self.oi.driver.getY(self.oi.driver.Hand.kLeft)))

            if self.oi.get_drivetrain_shift():
                self.drivetrain_mechanism.toggle_shift()

            if self.oi.get_drive_mode_switch():
                self.drivetrain.toggle_mode()

            if self.oi.get_start_drive_straight():
                self.drivetrain.start_drive_straight()

            # HATCHES
            if self.oi.get_hatch_grabber():
                self.hatch_mechanism.toggle_grab()

            if self.oi.get_hatch_rack():
                self.hatch_mechanism.toggle_extended()

            # CARGO
            cargo_power = self.oi.process_deadzone(self.oi.sysop.getY(self.oi.sysop.Hand.kLeft), robotmap.Tuning.CargoMechanism.deadzone)
            if cargo_power > 0:
                self.cargo_mechanism.raise_lift(cargo_power)
            if cargo_power < 0:
                self.cargo_mechanism.lower_lift(-cargo_power)

            if self.oi.get_cargo_lock():
                self.cargo_mechanism.toggle_lock()

            # SENSORS
            if self.oi.get_camera_switch():
                self.current_camera = 0 if self.current_camera == 1 else 1

            if self.oi.get_calibrate_pressure():
                self.pressure_sensor.calibrate_pressure()

            # SMARTDASHBOARD
            dash.putNumber("Calibrated Pressure: ", self.pressure_sensor.get_pressure())
            dash.putString("Grabber: ", "Grabbing" if self.hatch_grabber.state == HatchGrabberPositions.GRABBING else "Released")
            dash.putString("Rack: ", "Extended" if self.hatch_rack.state == HatchRackPositions.EXTENDED else "Retracted")            
            dash.putString("Drive Mode: ", "Arcade Drive" if self.drivetrain.drive_mode == DriveModes.ARCADEDRIVE else "Tank Drive")
            dash.putString("Current Angle: ", self.navx.getAngle())
            dash.putString("Current rotation: ", self.drivetrain.rotation)
            self.camera_table.putString("Selected Camera", f"{self.current_camera}")
        except:
            self.onException()

if __name__ == "__main__":
    wpilib.run(MyRobot)
