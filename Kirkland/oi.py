# oi.py
# process driver input

import math
import json
import os

import wpilib

class OI:
    def __init__(self):
        self.settings = {}
        self.load_settings()

        self.driver = wpilib.XboxController(0)
        self.sysop = wpilib.XboxController(1)

    def load_settings(self):
        default_settings = {
            # driver controls
            "shift_drivetrain": wpilib.XboxController.Button.kBumperRight,
            "drive_mode_switch": wpilib.XboxController.Button.kX,
            "camera_switch": wpilib.XboxController.Button.kB,
            "drive_straight": wpilib.XboxController.Button.kBumperLeft,

            # sysop controls
            "hatch_grabber": wpilib.XboxController.Button.kB,
            "hatch_rack": wpilib.XboxController.Button.kY,
            "cargo_lock": wpilib.XboxController.Button.kBumperLeft,
            "calibrate_pressure": wpilib.XboxController.Button.kStickLeft,

            # drive tuning
            "driver_deadzone": 0.1,
            "straight_angle": 30,
            "straight_deadzone_horizontal": 0.05,
            "straight_deadzone_vertical": 0.1
        }

        self.settings = default_settings

    def get_button_pressed(self, controller : wpilib.XboxController, button):
        return controller.getRawButtonPressed(button)

    def get_button_config_pressed(self, controller : wpilib.XboxController, button_name):
        return self.get_button_pressed(controller, self.settings[button_name])

    def get_button_config_held(self, controller: wpilib.XboxController, button_name):
        return controller.getRawButton(self.settings[button_name])

    def process_deadzone(self, i, deadzone):
        if i < -deadzone or i > deadzone:
            return i
        return 0

    def check_drivetrain_straight(self, x, y):
        '''check and see if the input falls within the range needed to make the robot drive in a straight line'''
        # print(f"{x}, {y}")
        # theta = math.degrees(math.atan2(-x, abs(y)))
        # return abs(theta) < self.settings["straight_angle"]
        return self.process_deadzone(abs(x), self.settings["straight_deadzone_horizontal"]) == 0 and self.process_deadzone(abs(y), self.settings["straight_deadzone_vertical"]) != 0

    def drivetrain_curve(self, i):
        deadzoned = self.process_deadzone(i, self.settings["driver_deadzone"])
        return deadzoned ** 3

    def get_drivetrain_shift(self):
        return self.get_button_config_pressed(self.driver, "shift_drivetrain")
    
    def get_drive_mode_switch(self):
        return self.get_button_config_pressed(self.driver, "drive_mode_switch")

    def get_drive_straight(self):
        return self.get_button_config_held(self.driver, "drive_straight")

    def get_camera_switch(self):
        return self.get_button_config_pressed(self.driver, "camera_switch")

    def get_hatch_grabber(self):
        return self.get_button_config_pressed(self.sysop, "hatch_grabber")

    def get_hatch_rack(self):
        return self.get_button_config_pressed(self.sysop, "hatch_rack")

    def get_cargo_lock(self):
        return self.get_button_config_pressed(self.sysop, "cargo_lock")

    def get_calibrate_pressure(self):
        return self.get_button_config_pressed(self.sysop, "calibrate_pressure")