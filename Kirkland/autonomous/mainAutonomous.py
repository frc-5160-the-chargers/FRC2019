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

class MainAutonomous:
    MODE_NAME = "Main autonomous"
    DEFAULT = True

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

    oi: OI
    navx: navx.AHRS

    def on_enable(self):
        """
        Called when the robot starts; optional
        """
        self.drivetrain_mechanism.reset()
        self.cargo_mechanism.reset()
        self.hatch_mechanism.reset()
        self.current_camera = 0
        self.hatch_mechanism.grab()

    def on_disable(self):
        pass
    
    def on_iteration(self, time_elapsed):
        """
        Called on each iteration of the control loop for both auton and tele
        """
        # TODO Since this is the same code as teleop, there should be some way to consolidate it into one function
        # TODO Individual try catches
        
        try:
            # DRIVETRAIN
            if self.drivetrain.drive_mode == DriveModes.ARCADEDRIVE:
                self.drivetrain.arcade_drive(self.oi.drivetrain_curve(self.oi.driver.getY(
                    self.oi.driver.Hand.kLeft)), -self.oi.driver.getX(self.oi.driver.Hand.kRight))
            elif self.drivetrain.drive_mode == DriveModes.TANKDRIVE:
                self.drivetrain.tank_drive(self.oi.drivetrain_curve(self.oi.driver.getY(
                    self.oi.driver.Hand.kLeft)), self.oi.drivetrain_curve(self.oi.driver.getY(self.oi.driver.Hand.kRight)))
            
            if self.navx.isConnected() and self.oi.check_drivetrain_straight(self.oi.driver.getX(self.oi.driver.Hand.kRight), self.oi.driver.getY(self.oi.driver.Hand.kLeft)):
                self.drivetrain.drive_straight(self.oi.drivetrain_curve(self.oi.driver.getY(self.oi.driver.Hand.kLeft)))
            elif self.drivetrain.drive_mode == DriveModes.DRIVETOANGLE:
                self.drivetrain.drive_mode = DriveModes.ARCADEDRIVE

            if self.oi.get_drivetrain_shift():
                self.drivetrain_mechanism.toggle_shift()

            # if self.oi.get_drive_mode_switch():
            #     self.drivetrain.toggle_mode()

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
            dash.putString("Grabber: ", self.hatch_grabber.state)
            dash.putString("Rack: ", self.hatch_rack.state)
            dash.putString("Drive Mode: ", self.drivetrain.drive_mode)
        except:
            self.onException()